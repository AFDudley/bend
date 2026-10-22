# Tag
# ===

# The tags are this module's spelling, from wherever the program sits.
def tag_off(k):
    return {"$": CID(Off)}

def tag_on(k):
    return {"$": CID(On), "n": 3}

io_eff(CID(tag.off), tag_off)
io_eff(CID(tag.on), tag_on)
