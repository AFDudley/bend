"""The Bend2 toolchain inside this wheel.

_data/ holds the fork's bend2/ tree at one commit, a bun binary, and a BendTT
kernel built with Lean (the version in _data/LEAN_VERSION). `bend --verdict`
runs that kernel through $BENDTT, so no Lean is needed at use.
"""

from __future__ import annotations

from pathlib import Path

DATA = Path(__file__).resolve().parent / "_data"
BUN = DATA / "bun"
BENDTT = DATA / "bendtt"
BEND_MAIN = DATA / "bend2" / "main.ts"


def _read(name: str) -> str:
    return (DATA / name).read_text().strip()


COMMIT = _read("COMMIT")
LEAN_VERSION = _read("LEAN_VERSION")
BUN_VERSION = _read("BUN_VERSION")


def argv() -> list[str]:
    """The argv prefix that runs the bend compiler under the bundled bun."""
    return [str(BUN), str(BEND_MAIN)]


def env(base: dict[str, str]) -> dict[str, str]:
    """`base` with $BENDTT set to the bundled kernel, unless `base` sets it,
    and the daily version check off."""
    out = dict(base)
    out.setdefault("BENDTT", str(BENDTT))
    out.setdefault("BEND_NO_TELEMETRY", "1")
    return out
