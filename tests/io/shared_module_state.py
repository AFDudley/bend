_count = [0]

def tick_bump(k):
    _count[0] += 1
    return _count[0] & 0xFFFFFFFF

def tick_peek(k):
    return _count[0] & 0xFFFFFFFF

io_eff(CID(Tick.bump), tick_bump)
io_eff(CID(Tick.peek), tick_peek)
