def dispose(f, k):
    if not callable(f):
        raise Exception("expected a retained closure")
    return 5

io_eff(CID(dispose), dispose)
