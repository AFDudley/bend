# A backslash does not continue a Python # comment, so the next line stays live.
def answer(k):
    return 42
# A path ending in a backslash, C:\, must not swallow the CID below: \
io_eff(CID(answer), answer)
