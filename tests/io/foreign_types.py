# Tree
# ====

# A balanced tree of the depth asked, its leaves 1.. left to right, every
# odd one Empty, as the C lays it.
def tree_make(depth, k):
    next_v = [0]
    def at(d):
        if d == 0:
            next_v[0] += 1
            n = next_v[0]
            return {"$": CID(Empty)} if n % 2 == 1 else {"$": CID(Leaf), "v": n}
        l = at(d - 1)
        return {"$": CID(Node), "l": l, "r": at(d - 1)}
    return at(int(depth))

# Chain
# =====

def chain_make(n, k):
    c = {"$": CID(End)}
    for i in range(int(n)):
        c = {"$": CID(Cell), "v": i, "next": c}
    return c

io_eff(CID(tree.make), tree_make)
io_eff(CID(chain.make), chain_make)
