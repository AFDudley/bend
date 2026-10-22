# File
# ====

def file_size(file, k):
    try:
        size = os.fstat(file).st_size
        over = 84 if sys.platform == "darwin" else 75
        return io_tup(file, io_fail(over) if size > 4294967295 else io_done(size))
    except OSError as e:
        return io_tup(file, io_fail(abs(e.errno if e.errno else 5)))

io_eff(CID(File.size), file_size)
