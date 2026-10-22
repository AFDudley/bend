# Set a variable whose value holds a "=", for get_env to look past.
def put_eq(k):
    os.environ["BEND_ENV_EQ"] = "x=y"
    return {"$": CID(Unit)}

io_eff(CID(put_eq), put_eq)
