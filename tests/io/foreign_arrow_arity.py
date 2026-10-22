def twice(x, k):
    return (2 * x) & 0xFFFFFFFF

io_eff(CID(twice), twice)
