def flags(par, seq, k):
    if not callable(par) or not callable(seq):
        raise Exception("expected retained functions")
    return {"$": CID(Unit)}

io_eff(CID(flags), flags)
