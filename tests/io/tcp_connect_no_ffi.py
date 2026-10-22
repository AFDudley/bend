# The JS twin poisons globalThis.BEND_SYS (JS's lazy bun:ffi binding) to
# pin that an invalid TCP.connect argument fails with EINVAL before any
# native call. This backend's tcp_connect.py validates the address with
# sock_addr_ok, pure Python, before it opens a socket; it has no FFI
# layer to poison. ffi_absent is a no-op; the same invariant (a bad
# address fails EINVAL, untouched by any native binding) holds for this
# backend by construction.
def ffi_absent_run(k):
    return {"$": CID(Unit)}

io_eff(CID(ffi_absent), ffi_absent_run)
