import shutil
import subprocess
import tempfile

# Output files must not overwrite inputs through a path, symlink or hard
# link. The compiler's own cli_file check is backend-agnostic; this twin
# repeats the JS twin's scenario with -o targets ending .py instead of
# .js.
def output_input_links(k):
    bun = shutil.which("bun") or os.path.expanduser("~/.bun/bin/bun")
    with tempfile.TemporaryDirectory(prefix="bend-output-input-") as dir:
        inputs = {
            "main.bend": "import Base\nimport ./lib.bend as Lib\n"
                'def Probe.value() -> IO(U32):\n'
                '  import "./effect.js"\n  import "./effect.c"\n'
                "def main() -> U32:\n  Lib.value()\n",
            "lib.bend": "import Base\ndef value() -> U32:\n  42\n",
            "effect.js": "io_eff(CID(Probe.value), () => 42);\n",
            "effect.c": "// Foreign input.\n",
        }
        paths = {name: os.path.join(dir, name) for name in inputs}
        main = paths["main.bend"]
        # effect.py is the Python twin; cli_file's own input-aliasing
        # check does not track it (ins comes from each def's .i list,
        # which only ever holds the .c/.js names the parser accepts), so
        # it is support here, not one of the paths this test asserts
        # against.
        effect_py = os.path.join(dir, "effect.py")
        env = {**os.environ, "HOME": dir, "BEND_ORIGIN": "http://127.0.0.1:9",
            "BEND_NO_TELEMETRY": "1"}

        def build(*outs):
            args = [bun, os.path.abspath("bend2/main.ts"), main]
            for out in outs:
                args += ["-o", out]
            return subprocess.run(args, capture_output=True, text=True,
                timeout=4, env=env)

        def intact():
            return all(open(paths[name]).read() == text
                for name, text in inputs.items())

        def rejects(got, msg):
            return got.returncode == 1 and msg in got.stderr and intact()

        for name, text in inputs.items():
            with open(paths[name], "w") as f:
                f.write(text)
        with open(effect_py, "w") as f:
            f.write("def probe_value(k):\n    return 42\n\n"
                "io_eff(CID(Probe.value), probe_value)\n")
        link = os.path.join(dir, "out.py")
        ok = os.path.join(dir, "ok.py")
        code = 1
        if not rejects(build(main), "is a file the program reads"):
            return code
        code += 1
        os.symlink(main, link)
        if not rejects(build(link), "is a file the program reads"):
            return code
        os.unlink(link)
        code += 1
        for name in inputs:
            os.link(paths[name], link)
            if not rejects(build(link), "is a file the program reads"):
                return code
            os.unlink(link)
            code += 1
        if not rejects(build(dir), "or a directory"):
            return code
        code += 1
        os.link(main, link)
        if (not rejects(build(ok, link), "is a file the program reads")
            or os.path.exists(ok)):
            return code
        os.unlink(link)
        code += 1
        built = build(ok)
        if built.returncode != 0 or not intact():
            return code
        ran = subprocess.run(["python3", ok], capture_output=True,
            text=True, timeout=4)
        if ran.returncode != 0 or ran.stdout.strip() != "42":
            return code
        return 0

io_eff(CID(Output.input_links), output_input_links)
