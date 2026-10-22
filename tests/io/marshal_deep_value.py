def list_new(k_count, k):
    out = {"$": CID(Nil)}
    for i in range(k_count - 1, -1, -1):
        out = {"$": CID(Con), "head": i & 0xff, "tail": out}
    return out

def list_sum(xs, k):
    n = 0
    while xs["$"] == CID(Con):
        n = (n + xs["head"]) & 0xffffffff
        xs = xs["tail"]
    return n

io_eff(CID(list_new), list_new)
io_eff(CID(list_sum), list_sum)
