import subprocess

# A child writes length bytes into a FIFO, then waits on an ack pipe and
# closes the FIFO only once the reader has drained it and parks again, so
# the reader's last wake is the close alone. The reader's end moves to fd
# hi when hi is nonzero.
def fifo_drain(length, hi, k):
    n = int(length)
    hi_fd = int(hi)
    path = "/tmp/bend_fifo_py_%d" % os.getpid()
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass
    os.mkfifo(path, 0o600)
    rd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    wr = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
    os.unlink(path)
    if hi_fd != 0:
        os.dup2(rd, hi_fd)
        os.close(rd)
        rd = hi_fd
    ack_r, ack_w = os.pipe()
    sh = 'printf %s "' + ("x" * n) + '"; head -c 1 >/dev/null'
    subprocess.Popen(["sh", "-c", sh], stdin=ack_r, stdout=wr)
    os.close(ack_r)
    os.close(wr)
    total = 0
    acked = False
    def go():
        nonlocal total, acked, rd
        while True:
            try:
                chunk = os.read(rd, 64)
            except BlockingIOError:
                if not acked and total == n:
                    os.close(ack_w)
                    acked = True
                io_park_on(rd, False, k, go, None)
                return PARKED
            if len(chunk) > 0:
                total += len(chunk)
                continue
            os.close(rd)
            return total
    return go()

io_eff(CID(fifo.drain), fifo_drain)
