# A host's -0 is unsigned zero as a U32 (Python ints have no signed
# zero), but retains its sign as an F32 (Python floats do).
def uint_zero(k):
    return 0

def float_zero(k):
    return -0.0

io_eff(CID(uint_zero), uint_zero)
io_eff(CID(float_zero), float_zero)
