# File
# ====

def file_write_buffer(file, b):
    at = 0
    try:
        while at < len(b):
            n = os.write(file, b[at:])
            # no progress would retry forever (#1445)
            if n == 0:
                return io_tup(file, io_fail(5))
            at += n
        return io_tup(file, io_done({"$": CID(Unit)}))
    except OSError as e:
        return io_tup(file, io_fail(abs(e.errno if e.errno else 5)))

def file_write(file, data, k):
    return file_write_buffer(file, io_bytes(data))

def file_write_bytes(file, data, k):
    b = io_unlist(data)
    return io_tup(file, io_fail(22)) if b is None else file_write_buffer(file, b)

io_eff(CID(File.write), file_write)
io_eff(CID(File.write_bytes), file_write_bytes)
