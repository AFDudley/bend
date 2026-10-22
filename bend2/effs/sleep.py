# IO
# ==

# Parks until ms milliseconds from now.
def io_sleep(ms, k):
    io_park_on(None, False, k, lambda: {"$": CID(Unit)},
        time.monotonic() * 1000 + float(ms))
    return PARKED

io_eff(CID(IO.sleep), io_sleep)
