# Socket
# ======

def socket_close(socket_v, k):
    sock_close(socket_v)
    return {"$": CID(Unit)}

io_eff(CID(Socket.close), socket_close)
