def low(k):
    return "\ud7ff"

def high(k):
    return "\ue000"

def apex(k):
    return "\U0010ffff"

def edge(k):
    return "\ud7ff"

def torn(k):
    return "a\ud800"

io_eff(CID(low), low)
io_eff(CID(high), high)
io_eff(CID(apex), apex)
io_eff(CID(edge), edge)
io_eff(CID(torn), torn)
