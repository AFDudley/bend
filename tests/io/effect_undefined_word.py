# The length of n copies of the word undefined, as the C counts it.
def word_len(n, k):
    return (n * len("undefined")) & 0xFFFFFFFF

io_eff(CID(word.len), word_len)
