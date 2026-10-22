def native_apply(step, value, k):
    return step(value)

io_eff(CID(native.apply), native_apply)
