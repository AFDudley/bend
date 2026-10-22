# UDP
# ===

# A datagram goes whole or not at all; a full send buffer (non-blocking,
# so EAGAIN) parks the computation until the socket is writable. b is the
# datagram's bytes, data the value a failed or late send hands back.
def udp_send_to_with(socket_v, host, port, data, b, k, at=None):
    def fail(code):
        return io_tup(socket_v, io_ready(at, io_fail(code, data)))
    if not sock_addr_ok(host, int(port)):
        return fail(22)
    fd = socket_v
    def go():
        try:
            sock_of(fd).sendto(b, (host, int(port)))
        except OSError as e:
            code = e.errno if e.errno else EAGAIN
            if code != EAGAIN:
                return fail(code)
            if io_late(at):
                return io_tup(socket_v, {"$": CID(Wait), "rest": data})
            io_park_on(fd, True, k, go, at)
            return PARKED
        return io_tup(socket_v, io_ready(at, io_done({"$": CID(Unit)})))
    return go()

# A value past 255 fails with EINVAL before the datagram is sent, list kept.
def udp_send_bytes_to_with(socket_v, host, port, data, k, at=None):
    b = io_unlist(data)
    if b is not None:
        return udp_send_to_with(socket_v, host, port, data, b, k, at)
    return io_tup(socket_v, io_ready(at, io_fail(22, data)))

def udp_send_to(socket_v, host, port, data, k):
    return udp_send_to_with(socket_v, host, port, data, io_bytes(data), k)

def udp_send_bytes_to(socket_v, host, port, data, k):
    return udp_send_bytes_to_with(socket_v, host, port, data, k)

# The try_ twins pass a deadline at: past it, a send that would wait is
# Wait{data}.
def udp_try_send_to(socket_v, host, port, data, ms, k):
    return udp_send_to_with(socket_v, host, port, data, io_bytes(data), k,
        io_until(ms))

def udp_try_send_bytes_to(socket_v, host, port, data, ms, k):
    return udp_send_bytes_to_with(socket_v, host, port, data, k, io_until(ms))

io_eff(CID(UDP.send_to), udp_send_to)
io_eff(CID(UDP.send_bytes_to), udp_send_bytes_to)
io_eff(CID(UDP.try_send_to), udp_try_send_to)
io_eff(CID(UDP.try_send_bytes_to), udp_try_send_bytes_to)
