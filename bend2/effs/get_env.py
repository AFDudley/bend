# IO
# ==

def io_get_env(name, k):
    name = str_out(name)
    # reject a NUL or a "=" in the name, like get_env.c (#1449)
    if "\0" in name or "=" in name:
        return io_fail(2)
    value = os.environ.get(name)
    return io_fail(2) if value is None else io_done(value)

io_eff(CID(IO.get_env), io_get_env)
