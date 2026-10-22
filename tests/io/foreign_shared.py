# A balanced tree of the depth asked, its leaves 1.. left to right, every
# odd one Empty, as the C lays it.
def shared_make(depth, k):
    next_v = [0]
    def at(d):
        if d == 0:
            next_v[0] += 1
            n = next_v[0]
            return {"$": CID(Empty)} if n % 2 == 1 else {"$": CID(Leaf), "v": n}
        l = at(d - 1)
        return {"$": CID(Node), "l": l, "r": at(d - 1)}
    return at(int(depth))

io_eff(CID(shared.make), shared_make)
