# TCP
# ===

# The request parks until the listener is readable, so a backlog never
# keeps the loop from its timers; an accept that still finds no connection
# (the listener is non-blocking) parks again. The accepted socket is
# non-blocking for life.
def tcp_accept_with(listener, k, at=None):
    lfd = listener
    def go():
        try:
            conn, _addr = sock_of(lfd).accept()
        except OSError as e:
            code = e.errno if e.errno else EAGAIN
            if code != EAGAIN:
                return io_tup(listener, io_ready(at, io_fail(code)))
            if io_late(at):
                return io_tup(listener, {"$": CID(Wait), "rest": {"$": CID(Unit)}})
            io_park_on(lfd, False, k, go, at)
            return None
        return io_tup(listener, io_ready(at, io_done(sock_reg(conn))))
    io_park_on(lfd, False, k, go, at)
    return None

def tcp_accept(listener, k):
    return tcp_accept_with(listener, k)

# try_ passes a deadline at: past it, an accept that would wait answers Wait{}.
def tcp_try_accept(listener, ms, k):
    return tcp_accept_with(listener, k, io_until(ms))

io_eff(CID(TCP.accept), tcp_accept)
io_eff(CID(TCP.try_accept), tcp_try_accept)
