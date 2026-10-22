# An interval timer has the kernel send SIGALRM ms later, whatever the
# loop is doing then. The handler installs here, at module load, on the
# main thread (signal.signal works only there); the timer itself arms
# from idle_park, on the IO thread, where setitimer is allowed. The
# computation then parks on the read end of a pipe whose write end
# stays open and unwritten: its fd never becomes ready, so a wake is
# spurious.
signal.signal(signal.SIGALRM, lambda *a: None)

def idle_park(ms, k):
    signal.setitimer(signal.ITIMER_REAL, int(ms) / 1000.0)
    pr, pw = os.pipe()
    os.set_blocking(pr, False)
    io_park_on(pr, False, k, lambda: {"$": CID(Unit)}, None)
    return PARKED

io_eff(CID(Idle.park), idle_park)
