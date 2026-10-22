# Chan
# ====

# Chan.new, send, recv, close and the try_ twins share this file.

# A parked receiver holds CHAN_RECV: the C lane parks TERM_HOLE, and a
# program can make neither. A sent value may be None (an erased proof).
CHAN_RECV = object()

def chan_done():
    return {"$": CID(Done), "value": {"$": CID(Unit)}}

def chan_wait(item):
    return {"$": CID(Wait),
        "rest": {"$": CID(Unit)} if item is CHAN_RECV else item}

# The first waiter, past those whose IO has returned (a nested io_run):
# their computations are gone with it, so the row drops them and their
# items.
def chan_head(row):
    while row["wait"] and row["wait"][0]["io"].get("done"):
        row["wait"].pop(0)
    return row["wait"][0] if row["wait"] else None

# Wakes the first live waiter with x, as Ready{x} if try_ (cutting its
# timer, if the poller has not taken it yet), on the IO that parked it: a
# nested io_run may wake an outer one.
def chan_wake(row, x):
    w = chan_head(row)
    row["wait"].pop(0)
    if w.get("late") is not None:
        ws = w["io"]["waits"]
        at = next((j for j, t in enumerate(ws) if t["more"] is w["late"]), -1)
        if at >= 0:
            ws.pop(at)
        x = {"$": CID(Ready), "value": x}
    io_push(w["cont"], x, False, w["io"])
    return w["item"]

def chan_take(row):
    v = row["ring"].pop(0)
    if chan_head(row) is not None:
        row["ring"].append(chan_wake(row, chan_done()))
    return v

# A handle is the row (a stale copy keeps it, shut).
def chan_shut(row):
    row["shut"] = True
    while chan_head(row) is not None:
        item = row["wait"][0]["item"]
        chan_wake(row, {"$": CID(None)} if item is CHAN_RECV
            else {"$": CID(Fail), "error": item})

# Parks k on row with item; with ms, a timer too, whose late answers Wait:
# the first of the two to come cuts the other.
def chan_park(row, k, item, ms=None):
    w = {"io": _io_active, "cont": k, "item": item, "late": None}
    if ms is not None:
        def late():
            at = next((j for j, t in enumerate(row["wait"]) if t is w), -1)
            if at < 0:
                return PARKED
            row["wait"].pop(at)
            return chan_wait(item)
        w["late"] = late
        io_park_on(None, False, k, late, io_until(ms))
    row["wait"].append(w)
    return PARKED

# Sends without waiting: Done{}, Fail{v} if closed, PARKED if it would park.
def chan_put(row, value):
    if row["shut"]:
        return {"$": CID(Fail), "error": value}
    head = chan_head(row)
    if head is not None and head["item"] is CHAN_RECV:
        chan_wake(row, {"$": CID(Some), "value": value})
        return chan_done()
    if len(row["ring"]) < row["room"]:
        row["ring"].append(value)
        return chan_done()
    return PARKED

# Receives without waiting: Some{v}, None{} at the end, PARKED if not ready.
def chan_get(row):
    if len(row["ring"]) > 0:
        return {"$": CID(Some), "value": chan_take(row)}
    w = chan_head(row)
    if w is not None and w["item"] is not CHAN_RECV:
        return {"$": CID(Some), "value": chan_wake(row, chan_done())}
    if row["shut"]:
        return {"$": CID(None)}
    return PARKED

# Ready{x} now, Wait{rest} now if ms is 0, else parks until a wake or ms.
def chan_try(row, x, item, ms, k):
    if x is not PARKED:
        return {"$": CID(Ready), "value": x}
    if int(ms) == 0:
        return chan_wait(item)
    return chan_park(row, k, item, int(ms))

def chan_new(room, k):
    return {"room": int(room), "ring": [], "wait": [], "shut": False}

def chan_send(row, value, k):
    x = chan_put(row, value)
    return x if x is not PARKED else chan_park(row, k, value)

def chan_recv(row, k):
    x = chan_get(row)
    return x if x is not PARKED else chan_park(row, k, CHAN_RECV)

def chan_try_send(row, value, ms, k):
    return chan_try(row, chan_put(row, value), value, ms, k)

def chan_try_recv(row, ms, k):
    return chan_try(row, chan_get(row), CHAN_RECV, ms, k)

def chan_close(row, k):
    if not row["shut"]:
        chan_shut(row)
    return {"$": CID(Unit)}

io_eff(CID(Chan.new), chan_new)
io_eff(CID(Chan.send), chan_send)
io_eff(CID(Chan.recv), chan_recv)
io_eff(CID(Chan.try_send), chan_try_send)
io_eff(CID(Chan.try_recv), chan_try_recv)
io_eff(CID(Chan.close), chan_close)
