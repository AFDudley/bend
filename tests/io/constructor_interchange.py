import subprocess
import shutil
import tempfile
import importlib

def constructor_interchange(k):
    bun = shutil.which("bun") or os.path.expanduser("~/.bun/bin/bun")
    with tempfile.TemporaryDirectory(prefix=".bend-constructor-interchange-", dir=os.getcwd()) as dir:
        with open(os.path.join(dir, "a.bend"), "w") as f:
            f.write(
"""import Base

type Counter is Data:
  Counter{count: Nat}

type Choice is Data:
  Left{count: Nat}
  Right{count: Nat}

type Flag is Data:
  Off{}
  On{}

def Counter.make() -> Counter: Counter{5n}
def Choice.left() -> Choice: Left{7n}
def Choice.right() -> Choice: Right{7n}
def Flag.off() -> Flag: Off{}
def Flag.on() -> Flag: On{}
""")
        with open(os.path.join(dir, "b.bend"), "w") as f:
            f.write(
"""import Base
import ./a.bend as A

def dec(c: A.Counter) -> Nat:
  A.Counter{count} = c
  Nat.sub(count, 1n)

def score(c: A.Choice) -> Nat:
  match c:
    case A.Left{count}: (count + 1n : Nat)
    case A.Right{count}: (count + 2n : Nat)

def flag(c: A.Flag) -> U32:
  match c:
    case A.Off{}: 0
    case A.On{}: 1
""")
        for name in ("a", "b"):
            built = subprocess.run([bun, os.path.abspath("bend2/main.ts"),
                os.path.join(dir, name + ".bend"), "-o",
                os.path.join(dir, name + ".pym")], capture_output=True,
                text=True, env={**os.environ, "HOME": dir,
                    "BEND_ORIGIN": "http://127.0.0.1:9"})
            if built.returncode != 0:
                return 1
            shutil.copyfile(os.path.join(dir, name + ".pym"),
                os.path.join(dir, name + ".py"))
        sys.path.insert(0, dir)
        try:
            A = importlib.import_module("a")
            B = importlib.import_module("b")
            return 0 if (B.dec(A.Counter_make()) == 4
                and B.score(A.Choice_left()) == 8
                and B.score(A.Choice_right()) == 9
                and B.flag(A.Flag_off()) == 0
                and B.flag(A.Flag_on()) == 1) else 1
        finally:
            sys.path.remove(dir)
            sys.modules.pop("a", None)
            sys.modules.pop("b", None)

io_eff(CID(Host.constructor_interchange), constructor_interchange)
