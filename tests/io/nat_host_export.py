import subprocess
import shutil
import tempfile
import importlib

def nat_host_export(k):
    bun = shutil.which("bun") or os.path.expanduser("~/.bun/bin/bun")
    with tempfile.TemporaryDirectory(prefix=".bend-nat-export-", dir=os.getcwd()) as dir:
        input_path = os.path.join(dir, "lib.bend")
        output = os.path.join(dir, "lib.pym")
        with open(input_path, "w") as f:
            f.write(
"""import Base

def identity(n: Nat) -> Nat:
  n

def inc(n: Nat) -> Nat:
  Nat.add(n, 1n)

def add(a: Nat, b: Nat) -> Nat:
  Nat.add(a, b)
""")
        built = subprocess.run([bun, os.path.abspath("bend2/main.ts"),
            input_path, "-o", output], capture_output=True, text=True,
            env={**os.environ, "HOME": dir, "BEND_ORIGIN": "http://127.0.0.1:9"})
        if built.returncode != 0:
            return 1
        sys.path.insert(0, dir)
        try:
            lib = importlib.import_module("lib")
            err = "bend: expected a Nat host number: an integer from 0 to 2^53"
            bad = [lambda: lib.inc(-1), lambda: lib.inc(1.5),
                lambda: lib.inc(2 ** 53 + 2), lambda: lib.add(1, -1),
                lambda: lib.identity(math.inf), lambda: lib.identity(math.nan)]
            for f in bad:
                try:
                    f()
                    return 2
                except Exception as e:
                    if str(e) != err:
                        return 2
            if lib.inc(41) != 42 or lib.add(2, 3) != 5:
                return 3
            return 0 if all(lib.identity(n) == n
                for n in (0, 2 ** 48, 2 ** 53)) else 3
        finally:
            sys.path.remove(dir)
            sys.modules.pop("lib", None)

io_eff(CID(Nat.host_export), nat_host_export)
