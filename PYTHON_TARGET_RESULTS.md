# Python target: measured results

Branch `python-target`, host kelce, `python3 3.12.3`, `bun 1.4.2`.
Produced by `gates/test_py_local.ts` (`WORKERS=16`), a local two-lane
runner: it builds `-o t.js` and `-o t.py` for every test under `tests/`
and runs each with a 5 s timeout, comparing output to the test's `#|`
lines. It is not `gates/test.ts`: that gate's four lanes (check,
interpret, JS, C) run on a mini cluster over SSH, which this host
cannot reach. This runner covers the JS and Python lanes only, on this
host.

## Totals

Total tests under `tests/`: 1,720.

| lane   | pass | fail | dropped |
|--------|------|------|---------|
| JS     | 870  | 5    | 845     |
| Python | 707  | 9    | 1004    |

A test is dropped when it has no runnable `main`, no `import Base`, or a
foreign def with no twin for that lane (print/print_err/args/args_bytes/
get_env/now ported to Python; every other effect — sleep, channels,
files, sockets, process, audio, window, random — has no `.py` twin, so a
test that imports one drops the Python lane, the same rule JS applies
for a missing `.js` twin).

The JS lane's pass/fail/dropped counts are unchanged by this branch: the
JS emitter, `OPERATIONS`, `OPTIMIZED`, `RuntimeJs` and `RUNTIME_MAIN` are
untouched; every edit to code JS also runs through is gated on
`FL.py`, false during a JS compile.

## Every Python failure where JS passes (7), by cause

### 1. Char past the Unicode scalars (4 tests)

Bend's `Char` is any 21-bit word, not only a Unicode scalar. The JS
runtime represents an out-of-range `Char` by packing it into 4 raw
UTF-16 units (a sentinel low surrogate plus three 11-bit pieces), which
works because a JS string indexes by UTF-16 unit. A Python `str`
indexes by codepoint, so the Python runtime represents a `Char` with
`chr()`/`ord()` directly: simpler and correct for every Unicode scalar,
but `chr()` raises for a value over `0x10FFFF`, and `str.encode("utf-8")`
raises for a lone surrogate. This is a real, understood gap in the
Python backend's Char representation, not chased in this spike.

Example: `tests/run/show_char_any_code.bend` —
`chr() arg not in range(0x110000)`.

Also: `io_print_non_scalar`, `run_map_bit_native` (uses `\u{ffffffff}`),
`base_string_contains`.

### 2. F32 bit-exact edge cases (2 tests)

`f32_round` (`F32.read` and a float literal) rounds a decimal to the
nearest f32 through `struct.pack`/`float()`, a double rounding (decimal
to f64, then f64 to f32) rather than the JS runtime's exact BigInt
comparison against the original decimal text. This differs only at a
f64/f32 rounding midpoint, which `tests/run/f32_read_round_once.bend`
is built to hit. Separately, `struct.pack`/`unpack` may quiet a
signaling NaN's bit pattern on round-trip, where the JS runtime (and C)
keep the bits exact, which `tests/compile/f32_table_nan_bits.bend`
checks for.

Example: `tests/run/f32_read_round_once.bend` — bit 1065353216 where
1065353215 is wanted (a decimal exactly at the f64/f32 midpoint rounds
to the wrong side).

### 3. Emitter bug: a long list literal overflows Python's parser (1 test)

A `List` literal with N elements compiles to N nested `{"$": "Con",
"head": ..., "tail": {...}}` dict literals, one level of nesting per
element (the JS emitter does the same, nested object literals, which
V8's parser accepts at this depth; CPython's parser does not).
`tests/base/u32_native_model.bend` builds a ~160-element list and trips
CPython's own parser recursion limit at compile time, before the program
even runs. A fix needs the Python emitter to build a long list through
statements (a loop, or chunked locals) instead of one nested expression,
which is a structural change out of scope for this spike.

Example: `tests/base/u32_native_model.bend` —
`MemoryError: Parser stack overflowed - Python source too complex to parse`.

## Not observed as a Python-only failure

Recursion depth: the host's native stack supports deep JS recursion
already, and the Python prelude (`sys.setrecursionlimit`,
`threading.stack_size`, in a new thread) kept every corpus test that
passes on JS inside its budget; no corpus test failed only on Python
with a stack-depth signature. An unported effect always shows as
*dropped*, not *failed*, by construction (the lane never builds), so no
unported-effect case appears in the failure list above.

## What the branch adds

- `bend2/comp.ts`: a `py` backend beside `js` — `py_var`, `py_call`,
  `py_open`, `py_expr`, `py_func`, `py_match`, `py_def`, `py_host`,
  `py_lib`, `py_book`, `py_text` (the brace-marker-to-indentation
  finalizer), `OPTIMIZED_PY`, and a `PY:` template for every op that has
  a `JS:` one. `Intr`, `file_new`/`FL`, `intr_of`, `emit_hold`,
  `emit_row`/`emit_tab`, `effect_src` and `c_ids` gained a third,
  `FL.py`-gated branch each; `block()`/`emit_chain()` are unchanged and
  reused verbatim, since `py_text` turns their existing " {"/"}" marker
  lines into Python indentation.
- `bend2/main.ts`: `-o x.py` calls `Comp.py_book`.
- `bend2/effs/{print,print_err,args,get_env,now}.py`: the five ported
  effects. `effect_src` finds a Python twin beside the `.js` one on
  disk (`effs/X.js` names `effs/X.py`), since bend.ts's parser accepts
  only a `.c` or `.js` import line and is human-written, not edited here.
- `gates/test_py_local.ts`: the local two-lane runner this report's
  numbers come from.
