# Audio
# =====

AUDIO_RING = 4096  # Frames; matches IO_RING in audio.c.

def audio_write(audio, samples, k):
    n = 0
    xs = samples
    while xs["$"] == CID(Con):
        n += 1
        xs = xs["tail"]
    frames = n // 2
    now = time.monotonic() * 1000
    drained = int((now - audio["at"]) * audio["rate"] / 1000)
    audio["queued"] = max(0, audio["queued"] - drained)
    # Carry subframe time while playing; idle time cannot drain future writes.
    audio["at"] = now if audio["queued"] == 0 or audio["rate"] == 0 \
        else audio["at"] + drained * 1000 / audio["rate"]
    # Complete stereo frames only; oversized writes are dropped whole.
    if n <= AUDIO_RING * 2 and audio["queued"] + frames <= AUDIO_RING:
        audio["queued"] += frames
    return io_tup(audio, audio["queued"])

io_eff(CID(Audio.write), audio_write)
