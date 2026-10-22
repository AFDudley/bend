# Far
# ===

# The tags are this module's file name, far_types, from wherever the
# program importing it sits.
def far_make(depth, k):
    next_v = [0]
    def at(d):
        if d == 0:
            next_v[0] += 1
            return {"$": CID(Near), "v": next_v[0]}
        l = at(d - 1)
        return {"$": CID(Deep), "l": l, "r": at(d - 1)}
    return at(int(depth))

io_eff(CID(far.make), far_make)
