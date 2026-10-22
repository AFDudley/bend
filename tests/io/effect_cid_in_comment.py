# The same quote, "CID(...) names no constructor or def", in the Python twin.
def answer(n, k):
    return (n + 2) & 0xFFFFFFFF

io_eff(CID(answer), answer)
