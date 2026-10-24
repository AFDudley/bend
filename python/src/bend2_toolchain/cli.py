"""The `bend` console script: run the bundled compiler under the bundled bun."""

from __future__ import annotations

import os
import sys

from bend2_toolchain import argv, env


def main() -> None:
    cmd = argv()
    os.execve(cmd[0], [*cmd, *sys.argv[1:]], env(dict(os.environ)))
