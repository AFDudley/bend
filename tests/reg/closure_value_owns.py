def heap_check(value, expected, before, k):
    if value != expected:
        raise Exception("closure_value_owns: incorrect sum")
    return 0

io_eff(CID(heap.check), heap_check)
