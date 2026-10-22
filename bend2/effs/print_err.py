# IO
# ==

def io_print_err(text, k):
    io_errs(text)
    return {"$": CID(Unit)}

io_eff(CID(IO.print_err), io_print_err)
