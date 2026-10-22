import subprocess
import shutil
import tempfile
import importlib

def _same(a, b):
    if math.isnan(a) and math.isnan(b):
        return True
    if a == 0 and b == 0:
        return math.copysign(1.0, a) == math.copysign(1.0, b)
    return a == b

def f32_host_export(k):
    bun = shutil.which("bun") or os.path.expanduser("~/.bun/bin/bun")
    with tempfile.TemporaryDirectory(prefix=".bend-f32-export-", dir=os.getcwd()) as dir:
        input_path = os.path.join(dir, "lib.bend")
        output = os.path.join(dir, "lib.pym")
        with open(input_path, "w") as f:
            f.write("import Base\n\ndef add(a: F32, b: F32) -> F32:\n"
                "  F32.add(a, b)\n")
        built = subprocess.run([bun, os.path.abspath("bend2/main.ts"),
            input_path, "-o", output], capture_output=True, text=True,
            env={**os.environ, "HOME": dir, "BEND_ORIGIN": "http://127.0.0.1:9"})
        if built.returncode != 0:
            return 1
        sys.path.insert(0, dir)
        try:
            lib = importlib.import_module("lib")
            pairs = [(16777217, 1), (-16777217, -1), (2 ** -150, 2 ** -149),
                (1.0000000596046448, 2 ** -24), (3.5e38, -3.5e38),
                (-0.0, -0.0), (math.inf, 1), (-math.inf, 1), (math.nan, 1)]
            for a, b in pairs:
                want = f32_rewrap(f32_rewrap(a) + f32_rewrap(b))
                if not _same(lib.add(a, b), want):
                    return 2
            return 0 if lib.add(16777217, 1) == 16777216 else 3
        finally:
            sys.path.remove(dir)
            sys.modules.pop("lib", None)

def f32_host_input(k):
    return 16777217

io_eff(CID(F32.host_export), f32_host_export)
io_eff(CID(F32.host_input), f32_host_input)
