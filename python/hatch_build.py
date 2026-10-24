"""Hatch build hook: tag the wheel for the platform its binaries need.

The wheel carries two native executables built by build.sh in a
debian:bookworm container: bun (the upstream linux-x64 release) and the
BendTT kernel (linked against glibc 2.36). So the wheel is not pure Python,
and its tag names the oldest glibc the kernel was linked against.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

PLATFORM_TAG = "py3-none-manylinux_2_36_x86_64"
REQUIRED = ("bun", "bendtt", "COMMIT", "LEAN_VERSION", "BUN_VERSION", "bend2/main.ts")


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        data = Path(self.root) / "src" / "bend2_toolchain" / "_data"
        missing = [name for name in REQUIRED if not (data / name).exists()]
        if missing:
            raise FileNotFoundError(f"run build.sh first; {data} lacks {missing}")
        build_data["pure_python"] = False
        build_data["tag"] = PLATFORM_TAG
