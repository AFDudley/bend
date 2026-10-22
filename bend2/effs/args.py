# IO
# ==

def io_args(k):
    xs = {"$": CID(Nil)}
    for i in range(len(cli_args) - 1, -1, -1):
        xs = {"$": CID(Con), "head": cli_args[i], "tail": xs}
    return xs

# Python already decodes argv as text, so a byte that is not UTF-8 arrives
# as U+FFFD's UTF-8, EF BF BD, same as the JS twin.
def io_args_bytes(k):
    xs = {"$": CID(Nil)}
    for i in range(len(cli_args) - 1, -1, -1):
        b = io_bytes(cli_args[i])
        xs = {"$": CID(Con), "head": io_list(b, len(b)), "tail": xs}
    return xs

io_eff(CID(IO.args), io_args)
io_eff(CID(IO.args_bytes), io_args_bytes)
