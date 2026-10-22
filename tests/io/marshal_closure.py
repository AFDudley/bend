def fold2(f, k):
    return f(f(1)(2))(3)

def pick_fn(m, k):
    if m["$"] == CID(Some):
        return m["value"](40)
    return 0

def stepper(k):
    return {"$": CID(Some), "value": lambda x: x + 100}

io_eff(CID(fold2), fold2)
io_eff(CID(pick_fn), pick_fn)
io_eff(CID(stepper), stepper)
