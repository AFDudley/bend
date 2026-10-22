#!/usr/bin/env bun
// A local two-lane runner for the python-target spike: builds -o t.js and
// -o t.py for every test under tests/, runs each with a timeout, and
// compares its output to the test's #| lines. gates/test.ts runs the real
// four-lane gate on the mini cluster, which this host cannot reach; this
// script only covers the JS and Python lanes, on this host, for the
// Python-backend measurement. The JS lane here is the reference: with no
// code change, its pass/fail/dropped counts must match a run before the
// Python backend was added.

import * as fs from "node:fs";
import * as path from "node:path";
import { execFile } from "node:child_process";

const ROOT = path.join(import.meta.dirname, "..");
const TESTS = path.join(ROOT, "tests");
const BUN = process.env.BUN_BIN ?? "/home/rix/.bun/bin/bun";
const PY = process.env.PYTHON_BIN ?? "python3";
const WORKERS = Number(process.env.WORKERS ?? 12);
const OUT_DIR = fs.mkdtempSync("/tmp/bend-pytest-");

type Test = {
  name: string;
  path: string;
  want: string;
  main: boolean;
  fails: boolean;
  base: boolean;
};

type Cls = "pass" | "fail" | "dropped";

type LaneResult = { name: string; cls: Cls; detail: string };

// tidy matches gates/test.ts: trailing blanks per line, then trim.
function tidy(text: string): string {
  return text.replace(/[ \t]+$/gm, "").trim();
}

// A program compiles only over Base (its IO runs main): a test without
// it checks and interprets alone, the same rule test_read in
// gates/test.ts applies to the js/c lanes.
const BASE_RE = /^(?:[\t\r ]*(?:(?:#|import[\t ])[^\n]*)?\n)*[\t ]*import[\t ]+Base(?=[\t\r ]*(?:#|\n|$))/;

function list_tests(): Test[] {
  const out: Test[] = [];
  const walk = (dir: string) => {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, ent.name);
      if (ent.isDirectory()) {
        walk(p);
      } else if (ent.name.endsWith(".bend")) {
        const rel = path.relative(TESTS, p);
        const src = fs.readFileSync(p, "utf8");
        const want = tidy(src.split("\n").filter((l) => l.startsWith("#|"))
          .map((l) => l.slice(2)).join("\n"));
        const main = /^(def|law) main(\(|:)/m.test(src);
        const fails = /^(SOME PROOFS FAIL|Error:)/.test(want);
        const base = BASE_RE.test(src);
        out.push({ name: rel.replace(/\.bend$/, "").replace(/\//g, "_"),
          path: p, want, main, fails, base });
      }
    }
  };
  walk(TESTS);
  return out;
}

function run(cmd: string, args: string[], timeoutMs: number,
  cwd = ROOT): Promise<{ out: string; code: number; timedOut: boolean }> {
  const { promise, resolve } = Promise.withResolvers<
    { out: string; code: number; timedOut: boolean }>();
  execFile(cmd, args, { cwd, timeout: timeoutMs, killSignal: "SIGKILL",
    maxBuffer: 32 * 1024 * 1024 }, (err, stdout, stderr) => {
    const e = err as (Error & { killed?: boolean; code?: number }) | null;
    resolve({ out: String(stdout) + String(stderr),
      code: e ? (e.code ?? 1) : 0, timedOut: !!e?.killed });
  });
  return promise;
}

// The build/run drop patterns match gates/test.ts's own two drop causes: a
// main the compiler refuses to print, and a foreign def with no twin for
// this lane (now three twins: .c, .js, .py).
const DROP_PATTERNS = [
  /a foreign def without a \.(js|py) import/,
  /no \.c import/,
  /a foreign def without a \.py twin/,
  /main's type .* cannot be printed/,
  /no main to run/,
];

async function build(test: Test, ext: "js" | "py"):
  Promise<{ ok: true; file: string } | { ok: false; dropped: boolean; msg: string }> {
  const outFile = path.join(OUT_DIR, test.name + "." + ext);
  const r = await run(BUN, ["bend2/main.ts", path.relative(ROOT, test.path),
    "-o", outFile], 20_000);
  if (r.code === 0 && fs.existsSync(outFile)) {
    return { ok: true, file: outFile };
  }
  const dropped = DROP_PATTERNS.some((re) => re.test(r.out));
  return { ok: false, dropped, msg: tidy(r.out) };
}

async function run_prog(ext: "js" | "py", file: string): Promise<string> {
  const cmd = ext === "js" ? BUN : PY;
  const r = await run(cmd, [file], 5000);
  let got = tidy(r.out);
  if (r.timedOut) {
    got = got === "" ? "timeout" : got + "\ntimeout";
  } else if (r.code !== 0) {
    got = got === "" ? "exit " + r.code : got + "\nexit " + r.code;
  }
  return got;
}

async function lane_run(test: Test, ext: "js" | "py"): Promise<LaneResult> {
  if (!test.main || test.fails) {
    return { name: test.name, cls: "dropped", detail: "no runnable main" };
  }
  if (!test.base) {
    return { name: test.name, cls: "dropped", detail: "no import Base" };
  }
  const b = await build(test, ext);
  if (!b.ok) {
    return { name: test.name, cls: b.dropped ? "dropped" : "fail", detail: b.msg };
  }
  const got = await run_prog(ext, b.file);
  return { name: test.name, cls: got === test.want ? "pass" : "fail", detail: got };
}

async function pool<T, R>(items: T[], n: number,
  f: (t: T) => Promise<R>): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let i = 0;
  let done = 0;
  async function worker() {
    while (i < items.length) {
      const idx = i++;
      results[idx] = await f(items[idx]);
      done += 1;
      if (done % 100 === 0) {
        console.error(`${done} / ${items.length}`);
      }
    }
  }
  await Promise.all(Array.from({ length: n }, worker));
  return results;
}

async function main(): Promise<void> {
  const all = list_tests();
  const limit = Number(process.env.LIMIT ?? 0);
  const tests = limit > 0 ? all.slice(0, limit) : all;
  console.error(`${tests.length} / ${all.length} tests under tests/`);
  console.error("running the JS lane...");
  const js = await pool(tests, WORKERS, (t) => lane_run(t, "js"));
  console.error("running the Python lane...");
  const py = await pool(tests, WORKERS, (t) => lane_run(t, "py"));
  fs.writeFileSync(path.join(ROOT, ".scratch", "py-local-results.json"),
    JSON.stringify({ total: tests.length, js, py }, null, 1));
  fs.rmSync(OUT_DIR, { recursive: true, force: true });
  console.error("done; wrote .scratch/py-local-results.json");
}

if (import.meta.main) {
  main();
}
