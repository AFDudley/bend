# Listener
# ========

def listener_close(listener, k):
    sock_close(listener)
    return {"$": CID(Unit)}

io_eff(CID(Listener.close), listener_close)
