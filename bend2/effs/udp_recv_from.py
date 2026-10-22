# UDP
# ===

# The request parks until the socket is readable, so a backlog never keeps
# the loop from its timers; a recv that still finds no datagram (the socket
# is non-blocking) parks again. The datagram, read makes a String (io_text)
# or a List of bytes (io_list).
def udp_recv_from_with(socket_v, max_n, k, read, at=None):
    if int(max_n) == 0:
        return io_tup(socket_v, io_ready(at, io_fail(22)))
    fd = socket_v
    # IPv4's 65535-byte packet has at least 20 IP and 8 UDP header bytes.
    size = min(int(max_n), 65507)
    def go():
        try:
            b, (host, port) = sock_of(fd).recvfrom(size)
        except OSError as e:
            code = e.errno if e.errno else EAGAIN
            if code != EAGAIN:
                return io_tup(socket_v, io_ready(at, io_fail(code)))
            if io_late(at):
                return io_tup(socket_v, {"$": CID(Wait), "rest": {"$": CID(Unit)}})
            io_park_on(fd, False, k, go, at)
            return None
        dgram = io_tup(host, port, read(b, len(b)))
        return io_tup(socket_v, io_ready(at, io_done(dgram)))
    io_park_on(fd, False, k, go, at)
    return None

def udp_recv_from(socket_v, max_n, k):
    return udp_recv_from_with(socket_v, max_n, k, io_text)

def udp_recv_bytes_from(socket_v, max_n, k):
    return udp_recv_from_with(socket_v, max_n, k, io_list)

# The try_ twins pass a deadline at: past it, a recv that would wait
# answers Wait{}.
def udp_try_recv_from(socket_v, max_n, ms, k):
    return udp_recv_from_with(socket_v, max_n, k, io_text, io_until(ms))

def udp_try_recv_bytes_from(socket_v, max_n, ms, k):
    return udp_recv_from_with(socket_v, max_n, k, io_list, io_until(ms))

io_eff(CID(UDP.recv_from), udp_recv_from)
io_eff(CID(UDP.recv_bytes_from), udp_recv_bytes_from)
io_eff(CID(UDP.try_recv_from), udp_try_recv_from)
io_eff(CID(UDP.try_recv_bytes_from), udp_try_recv_bytes_from)
