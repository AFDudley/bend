import subprocess
import shutil
import tempfile

def exit_status(k):
    bun = shutil.which("bun") or os.path.expanduser("~/.bun/bin/bun")
    with tempfile.TemporaryDirectory(prefix=".bend-exit-status-", dir=os.getcwd()) as dir:
        cases = [
            ("IO.exit(0)", 0, ""),
            ("IO.exit(255)", 255, ""),
            ("IO.exit(256)", 1, None),
            ("IO.exit(4294967295)", 1, None),
            ('IO.die(Unit, 7, "")', 7, "\n"),
            ('IO.die(Unit, 256, "reported")', 1, None, "reported\n"),
        ]
        for i, case in enumerate(cases):
            expression, status, stderr = case[0], case[1], case[2]
            start = case[3] if len(case) > 3 else None
            file = os.path.join(dir, "main.bend")
            out = os.path.join(dir, "main.py")
            with open(file, "w") as f:
                f.write("import Base\n\ndef main() -> IO(Unit):\n"
                    "  do IO<Unit>:\n    IO.print(\"before\")\n    "
                    + expression + "\n    IO.print(\"after\")\n")
            built = subprocess.run([bun, os.path.abspath("bend2/main.ts"),
                file, "-o", out], capture_output=True, text=True,
                env={**os.environ, "HOME": dir, "BEND_ORIGIN": "http://127.0.0.1:9"})
            if built.returncode != 0:
                return i + 1
            ran = subprocess.run(["python3", out], capture_output=True, text=True)
            if (ran.returncode != status or ran.stdout != "before\n"
                or (stderr is not None and ran.stderr != stderr)
                or (start is not None and not ran.stderr.startswith(start))):
                return i + 1
        return 0

io_eff(CID(Host.exit_status), exit_status)
