# IO
# ==

def io_write(text, k):
    io_out(1, io_bytes(text))
    return {"$": CID(Unit)}

io_eff(CID(IO.write), io_write)
