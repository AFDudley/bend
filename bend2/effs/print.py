# IO
# ==

def io_print(text, k):
    io_out(1, io_bytes(text + "\n"))
    return {"$": CID(Unit)}

io_eff(CID(IO.print), io_print)
