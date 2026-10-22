# File
# ====

_FILE_MODE = {"r": os.O_RDONLY, "w": os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
    "a": os.O_WRONLY | os.O_CREAT | os.O_APPEND}

# name is the path's bytes, or None if a value is past 255.
def file_open_with(name, mode):
    if name is None:
        return io_fail(22)
    if 0 in name:
        return io_fail(92 if sys.platform == "darwin" else 84)
    if mode not in _FILE_MODE:
        return io_fail(22)
    try:
        fd = os.open(bytes(name), _FILE_MODE[mode], 0o644)
        return io_done(fd)
    except OSError as e:
        return io_fail(abs(e.errno))

def file_open(path, mode, k):
    return file_open_with(io_bytes(path), mode)

def file_open_bytes(path, mode, k):
    return file_open_with(io_unlist(path), mode)

io_eff(CID(File.open), file_open)
io_eff(CID(File.open_bytes), file_open_bytes)
