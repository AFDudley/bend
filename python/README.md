# bend2-toolchain

The Bend2 compiler from this fork (with the Python target), packaged as one
platform wheel so a Python project can pin it in its lock file.

The wheel holds:

- `bend2/` from one commit of this repository (`_data/COMMIT`);
- bun, the upstream linux-x64 release (`_data/BUN_VERSION`), checked against
  the release's `SHASUMS256.txt`;
- `bendtt`, the BendTT kernel compiled from `bend2/bendtt.lean` with the Lean
  version that `bend2/safe.ts` names (`_data/LEAN_VERSION`).

The `bend` console script runs `bend2/main.ts` under the bundled bun with
`$BENDTT` set to the bundled kernel. So `bend x.bend --verdict` checks proofs
with the compiled Lean kernel and needs no Lean installation.

## Build

    python/build.sh

It needs git, docker and uv. The kernel and bun are fetched and built in
`debian:bookworm-slim`, so the wheel's tag is `manylinux_2_36_x86_64`.
The output is `python/dist/bend2_toolchain-<version>-py3-none-manylinux_2_36_x86_64.whl`.

To move to another commit, change `BEND_COMMIT` in `build.sh` and the
`+pytarget.<commit>` part of the version in `pyproject.toml`; `build.sh`
refuses when the two differ.
