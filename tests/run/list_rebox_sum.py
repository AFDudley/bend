def heap_check(value, expected, before, k):
    if value != expected:
        raise Exception("unexpected reboxing result")
    return 0

io_eff(CID(heap.check), heap_check)
