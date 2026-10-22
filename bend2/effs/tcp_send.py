# TCP
# ===

# Sends what is left; a full socket (non-blocking, so EAGAIN) parks the
# computation until the socket is writable, and the loop resumes here.
def tcp_send_with(socket_v, b, k, at=None):
    fd = socket_v
    def go(off):
        while off < len(b):
            try:
                n = sock_of(fd).send(b[off:])
            except OSError as e:
                code = e.errno if e.errno else EAGAIN
                if code != EAGAIN:
                    fail = io_fail(code, io_list(b[off:], len(b) - off))
                    return io_tup(socket_v, io_ready(at, fail))
                if io_late(at):
                    rest = io_list(b[off:], len(b) - off)
                    return io_tup(socket_v, {"$": CID(Wait), "rest": rest})
                io_park_on(fd, True, k, lambda: go(off), at)
                return PARKED
            off += n
        return io_tup(socket_v, io_ready(at, io_done({"$": CID(Unit)})))
    return go(0)

# A value past 255 fails with EINVAL before any byte is sent, list kept.
def tcp_send_bytes_with(socket_v, data, k, at=None):
    b = io_unlist(data)
    if b is not None:
        return tcp_send_with(socket_v, b, k, at)
    return io_tup(socket_v, io_ready(at, io_fail(22, data)))

def tcp_send(socket_v, data, k):
    return tcp_send_with(socket_v, io_bytes(data), k)

def tcp_send_bytes(socket_v, data, k):
    return tcp_send_bytes_with(socket_v, data, k)

# The try_ twins pass a deadline at: past it, a waiting send is Wait{rest}.
def tcp_try_send(socket_v, data, ms, k):
    return tcp_send_with(socket_v, io_bytes(data), k, io_until(ms))

def tcp_try_send_bytes(socket_v, data, ms, k):
    return tcp_send_bytes_with(socket_v, data, k, io_until(ms))

io_eff(CID(TCP.send), tcp_send)
io_eff(CID(TCP.send_bytes), tcp_send_bytes)
io_eff(CID(TCP.try_send), tcp_try_send)
io_eff(CID(TCP.try_send_bytes), tcp_try_send_bytes)
