def flop(b, k):
    return not b

def loose(c, k):
    return "t" if c else 1

io_eff(CID(flop), flop)
io_eff(CID(loose), loose)
