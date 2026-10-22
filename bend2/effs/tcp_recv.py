# TCP
# ===

# A recv that finds nothing (the socket is non-blocking) parks until the
# socket is readable. What it finds, read makes a String (io_text) or a
# List of bytes (io_list).
def tcp_recv_with(socket_v, max_n, k, read, at=None):
    if int(max_n) == 0:
        return io_tup(socket_v, io_ready(at, io_fail(22)))
    fd = socket_v
    def go():
        try:
            b = sock_of(fd).recv(int(max_n))
        except OSError as e:
            code = e.errno if e.errno else EAGAIN
            if code != EAGAIN:
                return io_tup(socket_v, io_ready(at, io_fail(code)))
            if io_late(at):
                return io_tup(socket_v, {"$": CID(Wait), "rest": {"$": CID(Unit)}})
            io_park_on(fd, False, k, go, at)
            return PARKED
        got = {"$": CID(None)} if len(b) == 0 \
            else {"$": CID(Some), "value": read(b, len(b))}
        return io_tup(socket_v, io_ready(at, io_done(got)))
    return go()

def tcp_recv(socket_v, max_n, k):
    return tcp_recv_with(socket_v, max_n, k, io_text)

def tcp_recv_bytes(socket_v, max_n, k):
    return tcp_recv_with(socket_v, max_n, k, io_list)

# The try_ twins pass a deadline at: past it, a recv that would wait is Wait{}.
def tcp_try_recv(socket_v, max_n, ms, k):
    return tcp_recv_with(socket_v, max_n, k, io_text, io_until(ms))

def tcp_try_recv_bytes(socket_v, max_n, ms, k):
    return tcp_recv_with(socket_v, max_n, k, io_list, io_until(ms))

io_eff(CID(TCP.recv), tcp_recv)
io_eff(CID(TCP.recv_bytes), tcp_recv_bytes)
io_eff(CID(TCP.try_recv), tcp_try_recv)
io_eff(CID(TCP.try_recv_bytes), tcp_try_recv_bytes)
