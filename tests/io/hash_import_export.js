function hash_import_export() {
  const fs = require("node:fs");
  const path = require("node:path");
  const child = require("node:child_process");
  const dir = fs.mkdtempSync(path.join(process.cwd(), ".bend-hash-export-"));
  try {
    const pkg = path.join(dir, ".bend", "lib",
      "0xdeadbeefdeadbeefdeadbeefdeadbeef");
    fs.mkdirSync(pkg, { recursive: true });
    fs.writeFileSync(path.join(pkg, "mod.bend"), `import Base

def add_one(n: Nat) -> Nat:
  Nat.add(n, 1n)
`);
    const input = path.join(dir, "lib.bend");
    const output = path.join(dir, "lib.mjs");
    fs.writeFileSync(input, `import Base
import 0xdeadbeefdeadbeefdeadbeefdeadbeef/mod.bend as M

def call(n: Nat) -> Nat:
  M.add_one(n)
`);
    const built = child.spawnSync(process.execPath,
      [path.resolve("bend2/main.ts"), input, "-o", output], {
        encoding: "utf8",
        env: { ...process.env, HOME: dir, BEND_ORIGIN: "http://127.0.0.1:9" },
      });
    if (built.status !== 0) {
      return 1;
    }
    const lib = require(output).default;
    return lib.call(41) === 42 ? 0 : 2;
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

io_eff(CID(Hash.import_export), hash_import_export);
