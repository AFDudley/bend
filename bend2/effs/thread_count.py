# IO
# ==

# A Python program, like the JS lane, runs its io_run loop on one thread.
def io_thread_count(k):
    return 1

io_eff(CID(IO.thread_count), io_thread_count)
