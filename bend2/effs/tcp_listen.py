# TCP
# ===

def tcp_listen(host, port, k):
    if not sock_addr_ok(host, int(port)):
        return io_fail(22)
    try:
        s = _socketlib.socket(_socketlib.AF_INET, _socketlib.SOCK_STREAM)
        s.setsockopt(_socketlib.SOL_SOCKET, _socketlib.SO_REUSEADDR, 1)
        s.bind((host, int(port)))
        s.listen(512)
        return io_done(sock_reg(s))
    except OSError as e:
        return io_fail(abs(e.errno))

io_eff(CID(TCP.listen), tcp_listen)
