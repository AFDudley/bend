# The JS twin poisons globalThis.BEND_SYS (JS's lazy bun:ffi binding) to
# pin that File.size never touches it on its success path. This backend
# has no FFI binding at all: file_size.py reads a file's size through
# os.fstat and its EOVERFLOW errno through sys.platform, both native
# Python with no FFI layer to poison. ffi_absent and ffi_back are no-ops;
# the same invariant (a good file's size answers Done, untouched by any
# native binding) holds for this backend by construction.
def ffi_absent_run(k):
    return {"$": CID(Unit)}

def ffi_back_run(k):
    return {"$": CID(Unit)}

io_eff(CID(ffi_absent), ffi_absent_run)
io_eff(CID(ffi_back), ffi_back_run)
