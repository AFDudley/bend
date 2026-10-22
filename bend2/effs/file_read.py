# File
# ====

def file_read_with(file, max_n, offset, pack):
    length = min(int(max_n), 2147483647)
    try:
        b = os.pread(file, max(length, 1), offset) if offset is not None \
            else os.read(file, max(length, 1))
        return io_tup(file, io_done(pack(b, len(b))))
    except OSError as e:
        return io_tup(file, io_fail(abs(e.errno)))

def file_read(file, max_n, k):
    return file_read_with(file, max_n, None, io_text)

def file_read_bytes(file, max_n, k):
    return file_read_with(file, max_n, None, io_list)

def file_read_at(file, offset, max_n, k):
    return file_read_with(file, max_n, int(offset), io_list)

io_eff(CID(File.read), file_read)
io_eff(CID(File.read_bytes), file_read_bytes)
io_eff(CID(File.read_at), file_read_at)
