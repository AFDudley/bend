def keep(f, k):
    if not callable(f):
        raise Exception("expected a retained closure")
    return 1

io_eff(CID(keep), keep)
