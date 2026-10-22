def host_channel(c, mode, k):
    def build(cont):
        if mode == 2:
            return {"$": CID(Chan.recv), "args": [c], "kont": cont}
        if mode == 3:
            return {"$": CID(Chan.close), "args": [c], "kont": cont}
        return {"$": CID(Chan.send), "args": [c, 7], "kont": cont}
    code = io_run(lambda: build)
    if code != 0:
        raise Exception("nested channel IO failed")
    return {"$": CID(Unit)}

io_eff(CID(Host.channel), host_channel)
