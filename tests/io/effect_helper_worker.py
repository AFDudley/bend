asked = False

def a_run(ms, k):
    nonlocal asked
    a_run_helper()
    value = 11 if asked else 99
    asked = False
    return value

def a_run_helper():
    nonlocal asked
    asked = True

io_eff(CID(A.run), a_run)
