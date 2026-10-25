import subprocess
import shutil
import tempfile
import importlib

def hash_import_export(k):
    bun = shutil.which("bun") or os.path.expanduser("~/.bun/bin/bun")
    with tempfile.TemporaryDirectory(prefix=".bend-hash-export-", dir=os.getcwd()) as tmp:
        pkg = os.path.join(tmp, ".bend", "lib",
            "0xdeadbeefdeadbeefdeadbeefdeadbeef")
        os.makedirs(pkg)
        with open(os.path.join(pkg, "mod.bend"), "w") as f:
            f.write("import Base\n\ndef add_one(n: Nat) -> Nat:\n"
                "  Nat.add(n, 1n)\n")
        input_path = os.path.join(tmp, "lib.bend")
        output = os.path.join(tmp, "lib.pym")
        with open(input_path, "w") as f:
            f.write(
                "import Base\n"
                "import 0xdeadbeefdeadbeefdeadbeefdeadbeef/mod.bend as M\n\n"
                "def call(n: Nat) -> Nat:\n"
                "  M.add_one(n)\n")
        built = subprocess.run([bun, os.path.abspath("bend2/main.ts"),
            input_path, "-o", output], capture_output=True, text=True,
            env={**os.environ, "HOME": tmp, "BEND_ORIGIN": "http://127.0.0.1:9"})
        if built.returncode != 0:
            return 1
        raw = os.path.join(tmp, "lib.py")
        with open(raw) as f:
            src = f.read()
        if re.search(r"^def 0", src, re.M):
            return 2
        sys.path.insert(0, tmp)
        try:
            lib = importlib.import_module("lib")
            exported = [n for n in dir(lib) if n.endswith("add_one")
                and not n.startswith("__")]
            if len(exported) != 1:
                return 3
            direct = getattr(lib, exported[0])
            return 0 if direct(41) == 42 and lib.call(41) == 42 else 4
        finally:
            sys.path.remove(tmp)
            sys.modules.pop("lib", None)

io_eff(CID(Hash.import_export), hash_import_export)
