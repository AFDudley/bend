def five(k):
    return 5

def zero(k):
    return 0

def wrap(k):
    return {"$": CID(Some), "value": 9}

def dub(n, k):
    return n * 2

def flip(b, k):
    return not b

def ord(k):
    return {"$": CID(EQ)}

io_eff(CID(five), five)
io_eff(CID(zero), zero)
io_eff(CID(wrap), wrap)
io_eff(CID(dub), dub)
io_eff(CID(flip), flip)
io_eff(CID(ord), ord)
