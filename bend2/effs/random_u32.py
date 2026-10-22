# IO
# ==

def io_random_u32(k):
    try:
        return io_done(int.from_bytes(os.urandom(4), "little"))
    except OSError:
        return io_fail(5)

io_eff(CID(IO.random_u32), io_random_u32)
