# Window
# ======

def window_frame(window, image, k):
    return io_tup(window, image, {"$": CID(Nil)})

io_eff(CID(Window.frame), window_frame)
