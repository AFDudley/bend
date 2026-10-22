# UDP
# ===

def udp_bind(host, port, k):
    if not sock_addr_ok(host, int(port)):
        return io_fail(22)
    try:
        s = _socketlib.socket(_socketlib.AF_INET, _socketlib.SOCK_DGRAM)
        s.bind((host, int(port)))
        return io_done(sock_reg(s))
    except OSError as e:
        return io_fail(abs(e.errno))

io_eff(CID(UDP.bind), udp_bind)
