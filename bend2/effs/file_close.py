# File
# ====

def file_close(file, k):
    try:
        os.close(file)
    except OSError:
        pass
    return {"$": CID(Unit)}

io_eff(CID(File.close), file_close)
