#!/bin/sh
# Build the bend2-toolchain wheel. See python/README.md.
#
# Inputs, all pinned here:
#   - BEND_COMMIT: the commit whose bend2/ tree the wheel carries;
#   - BUN_VERSION: the upstream bun release, checked against its SHASUMS256.txt;
#   - LEAN_VERSION: the Lean toolchain that compiles bend2/bendtt.lean, the
#     version bend2/safe.ts names as LEAN_VERSION.
# The kernel is built in debian:bookworm (glibc 2.36), the glibc the wheel's
# platform tag names. Output: python/dist/bend2_toolchain-*.whl.
set -eu

BEND_COMMIT=cefaf5450
BUN_VERSION=1.4.2
LEAN_VERSION=4.34.0
IMAGE=debian:bookworm-slim

here=$(cd "$(dirname "$0")" && pwd)
repo=$(git -C "$here" rev-parse --show-toplevel)
data="$here/src/bend2_toolchain/_data"

full=$(git -C "$repo" rev-parse "$BEND_COMMIT^{commit}")
grep -q "pytarget.$BEND_COMMIT\"" "$here/pyproject.toml" \
  || { echo "pyproject.toml version does not name $BEND_COMMIT" >&2; exit 1; }
src_lean=$(git -C "$repo" show "$full:bend2/safe.ts" | sed -n 's/^const LEAN_VERSION = "\(.*\)";$/\1/p')
[ "$src_lean" = "$LEAN_VERSION" ] \
  || { echo "bend2/safe.ts at $BEND_COMMIT names Lean $src_lean, not $LEAN_VERSION" >&2; exit 1; }

rm -rf "$data" "$here/dist"
mkdir -p "$data"
git -C "$repo" archive "$full" bend2 | tar -x -C "$data"
echo "$full" > "$data/COMMIT"
echo "$LEAN_VERSION" > "$data/LEAN_VERSION"
echo "$BUN_VERSION" > "$data/BUN_VERSION"

docker run --rm -v "$data:/out" -e BUN_VERSION="$BUN_VERSION" -e LEAN_VERSION="$LEAN_VERSION" \
  "$IMAGE" sh -euc '
apt-get update -qq
apt-get install -y -qq --no-install-recommends curl ca-certificates unzip >/dev/null
cd /tmp
base=https://github.com/oven-sh/bun/releases/download/bun-v$BUN_VERSION
curl -fsSLO "$base/bun-linux-x64.zip"
curl -fsSLO "$base/SHASUMS256.txt"
grep " bun-linux-x64.zip\$" SHASUMS256.txt | sha256sum -c -
unzip -q bun-linux-x64.zip
install -m 755 bun-linux-x64/bun /out/bun
[ "$(/out/bun --version)" = "$BUN_VERSION" ]
curl -fsSL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
  | sh -s -- -y --no-modify-path --default-toolchain "leanprover/lean4:v$LEAN_VERSION" >/dev/null
export PATH=/root/.elan/bin:$PATH
lean --version | grep -q "version $LEAN_VERSION,"
mkdir -p /tmp/k && cp /out/bend2/bendtt.lean /tmp/k/ && cd /tmp/k
lean -c bendtt.c bendtt.lean
leanc -O3 -DNDEBUG bendtt.c -o /out/bendtt
chown -R '"$(id -u):$(id -g)"' /out
'

uv build --wheel --out-dir "$here/dist" "$here"
ls -l "$here/dist"
