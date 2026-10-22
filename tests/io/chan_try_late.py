# Blocks the loop for ms milliseconds inside one effect.
def hold(ms, k):
    time.sleep(ms / 1000)
    return {"$": CID(Unit)}

io_eff(CID(hold), hold)
