def box_val(b, k):
    return b["val"]

def box_new(k):
    return {"$": CID(MkBox), "val": 99}

io_eff(CID(box_val), box_val)
io_eff(CID(box_new), box_new)
