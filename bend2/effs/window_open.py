# Window
# ======

def window_open(title, width, height, k):
    code = 45 if sys.platform == "darwin" else 95
    text = ("Window.open: no display (build a native binary with bend "
        "<file> -o <out> and run it from a desktop session)")
    return {"$": CID(Fail), "error": io_tup(code, text)}

io_eff(CID(Window.open), window_open)
