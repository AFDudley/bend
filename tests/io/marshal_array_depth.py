def exchange(tree, k):
    want = 123456789
    node = tree
    depth = 0
    while node["$"] == CID(Node):
        if node["n"] != want or len(node["kids"]) != 1:
            raise Exception("invalid Node at depth " + str(depth))
        node = node["kids"][0]
        depth += 1
    if node["$"] != CID(Leaf) or node["n"] != want or depth != 20000:
        raise Exception("invalid Leaf at depth " + str(depth))
    node["n"] = 987654321
    return tree

io_eff(CID(exchange), exchange)
