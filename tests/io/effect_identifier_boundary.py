# Python cannot spell JS's $ or U+200D inside an identifier (CPython's
# tokenizer refuses both), so this twin uses Python's own legal boundary
# characters instead: a leading underscore (Pythonic privacy) and a
# Unicode letter, plus a name-mangled private class method for the #
# private-field case.
def _CID(n):
    return n + 1

def πCID(n):
    return n + 1

def __CID(n):
    return n + 1

class Counter:
    def __CID(self, n):
        return n + 1
    def value(self):
        return self.__CID(10)

def answer(k):
    if FID(helper) != "helper":
        raise Exception("wrong foreign function name")
    return _CID(9) + πCID(10) + __CID(9) + Counter().value()

io_eff(CID(answer), answer)
