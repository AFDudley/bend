# The cases run only in the Linux C lane.
def audio_test_count(k):
    return 0

def audio_test_start(i, k):
    return {"$": CID(Unit)}

def audio_test_wait(k):
    return {"$": CID(Unit)}

def audio_test_closed(k):
    return {"$": CID(Unit)}

io_eff(CID(AudioTest.count), audio_test_count)
io_eff(CID(AudioTest.start), audio_test_start)
io_eff(CID(AudioTest.wait), audio_test_wait)
io_eff(CID(AudioTest.closed), audio_test_closed)
