# Keep the real non-blocking send partial before the reader starts.
def small_send(socket_v, k):
    sock_of(socket_v).setsockopt(_socketlib.SOL_SOCKET, _socketlib.SO_SNDBUF, 1024)
    return socket_v

io_eff(CID(Host.small_send), small_send)
