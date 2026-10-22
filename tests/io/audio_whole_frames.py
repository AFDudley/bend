# Pause only this silent device, leaving the process clock untouched.
def audio_pause(audio, k):
    if "rate" not in audio:
        raise Exception("audio_whole_frames: missing Audio rate field")
    audio["rate"] = 0
    return audio

io_eff(CID(pause), audio_pause)
