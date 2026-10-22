# Mode 0 parks a sender of 99, 1 a timed receiver, 2 a receiver; then the
# nested IO fails, taking that waiter with it.
def host_inner(c, mode, k):
    def park(pk):
        if mode == 0:
            return {"$": CID(Chan.send), "args": [c, 99], "kont": pk}
        if mode == 1:
            return {"$": CID(Chan.try_recv), "args": [c, 5], "kont": pk}
        return {"$": CID(Chan.recv), "args": [c], "kont": pk}

    def spawned(pk):
        def after_park(x):
            return {"$": CID(IO.print), "args": ["dead waiter resumed"], "kont": pk}
        return park(after_park)

    def boom():
        raise Exception("inner failed")

    def after_spawn(x):
        return {"$": CID(IO.sleep), "args": [1], "kont": lambda x2: boom()}

    try:
        io_run(lambda: lambda cont: {
            "$": CID(IO.spawn), "args": [spawned], "kont": after_spawn})
        raise Exception("nested IO did not fail")
    except Exception as e:
        if str(e) != "inner failed":
            raise
    return {"$": CID(Unit)}

io_eff(CID(Host.inner), host_inner)
