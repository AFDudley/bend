def host_nested(mode, k):
    if mode == 0:
        code = io_run(lambda: lambda cont: {
            "$": CID(IO.print), "args": ["inner"], "kont": cont})
        if code != 0:
            raise Exception("nested IO failed")
    else:
        try:
            def boom(x=None):
                raise Exception("expected nested error")
            io_run(lambda: boom)
            raise Exception("nested IO did not fail")
        except Exception as e:
            if str(e) != "expected nested error":
                raise
    return {"$": CID(Unit)}

io_eff(CID(Host.nested), host_nested)
