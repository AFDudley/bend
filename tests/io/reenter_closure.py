def wrap(g, k):
    return lambda x: (g(x) + 100) & 0xFFFFFFFF

io_eff(CID(wrap), wrap)
