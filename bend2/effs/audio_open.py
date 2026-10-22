# Audio
# =====

# A silent device: the ring's queue drains by the clock.
def audio_open(rate, k):
    if rate < 8000 or rate > 192000:
        return io_fail(22)
    # tests/io/audio_whole_frames.bend pauses its device through the rate
    # field.
    return io_done({"rate": rate, "queued": 0, "at": time.monotonic() * 1000})

io_eff(CID(Audio.open), audio_open)
