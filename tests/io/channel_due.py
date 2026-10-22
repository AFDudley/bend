def receive(c, k):
    def send_kont(x):
        raise Exception("the send parked")
    def more():
        _io_eff[CID(Chan.send)](c, 7, send_kont)
    io_park_on(None, False, k, more, io_until(1))
    answer = _io_eff[CID(Chan.try_recv)](c, 10, k)
    time.sleep(0.02)
    return answer

io_eff(CID(Host.receive), receive)
