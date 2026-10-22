# Every nonempty write to the fd Stall.open answers makes no progress.
def stall_open(k):
    fd = os.open("/dev/null", os.O_WRONLY)
    real_write = os.write
    def stalled_write(f, data):
        return 0 if f == fd and len(data) > 0 else real_write(f, data)
    os.write = stalled_write
    return io_done(fd)

io_eff(CID(Stall.open), stall_open)
