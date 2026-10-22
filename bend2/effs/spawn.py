# IO
# ==

def io_spawn(act, k):
    io_push(act, lambda x: {"$": CID(Emit), "value": x}, True, _io_active)
    return {"$": CID(Unit)}

io_eff(CID(IO.spawn), io_spawn)
