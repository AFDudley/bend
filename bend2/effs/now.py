# IO
# ==

import time

def io_now(k):
    return int(time.monotonic() * 1000)

io_eff(CID(IO.now), io_now)
