def getc(k):
    return "A"

def pick(k):
    return {"$": CID(Some), "value": 90}

def stamp(k):
    return {"$": CID(Tuple), "fst": 113, "snd": "ok"}

io_eff(CID(getc), getc)
io_eff(CID(pick), pick)
io_eff(CID(stamp), stamp)
