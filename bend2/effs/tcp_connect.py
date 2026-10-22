# TCP
# ===

# The socket is non-blocking for life: EINPROGRESS parks the computation
# until the socket is writable, and then SO_ERROR says how the connect ended.
def tcp_connect(host, port, k):
    if not sock_addr_ok(host, int(port)):
        return io_fail(22)
    s = _socketlib.socket(_socketlib.AF_INET, _socketlib.SOCK_STREAM)
    s.setblocking(False)
    fd = s.fileno()

    def end(code):
        if code != 0:
            _sockets.pop(fd, None)
            try:
                s.close()
            except OSError:
                pass
            return io_fail(code)
        _sockets[fd] = s
        return io_done(fd)

    def error():
        return s.getsockopt(_socketlib.SOL_SOCKET, _socketlib.SO_ERROR)

    try:
        s.connect((host, int(port)))
        code = 0
    except BlockingIOError:
        code = EINPROGRESS
    except OSError as e:
        code = e.errno if e.errno else 5
    if code != EINPROGRESS:
        return end(code)
    _sockets[fd] = s
    io_park_on(fd, True, k, lambda: end(error()), None)
    return PARKED

io_eff(CID(TCP.connect), tcp_connect)
