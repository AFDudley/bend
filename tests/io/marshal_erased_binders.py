def scale(x, k):
    return x + 100

def apply7(f, k):
    return f(7)

io_eff(CID(scale), scale)
io_eff(CID(apply7), apply7)
