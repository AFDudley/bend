def _is_number(v):
    return isinstance(v, int) and not isinstance(v, bool)

def top(p, k):
    return "number" if _is_number(p["snd"]) else "other"

def deep(p, k):
    return "number" if _is_number(p["snd"]["snd"]) else "other"

io_eff(CID(top), top)
io_eff(CID(deep), deep)
