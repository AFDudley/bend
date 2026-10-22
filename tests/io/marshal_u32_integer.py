def zero(k):
    return 0

def full(k):
    return 4294967295

def frac(k):
    # Python's U32 is a plain int, with no implicit float coercion the
    # way a JS Number has; the host boundary truncates here, as JS's
    # own eventual bitwise read of this value would.
    return int(4.5) & 0xFFFFFFFF

io_eff(CID(zero), zero)
io_eff(CID(full), full)
io_eff(CID(frac), frac)
