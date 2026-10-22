# Process
# =======

import subprocess

# Reads stdout and stderr incrementally against a wall-clock deadline, so
# a child that exits but leaves a grandchild holding the pipe open (a
# backgrounded "sleep 3 &") never blocks a read past the deadline, and an
# output past max_output cuts the read short instead of buffering it all.
def _process_read(proc, max_n, deadline):
    outs = {proc.stdout.fileno(): bytearray(), proc.stderr.fileno(): bytearray()}
    live = set(outs.keys())
    size = 0
    over = False
    while live:
        left = deadline - time.monotonic()
        if left <= 0:
            return None, None, True, over
        ready, _, _ = select.select(list(live), [], [], left)
        if not ready:
            continue
        for fd in ready:
            chunk = os.read(fd, 65536)
            if chunk == b"":
                live.discard(fd)
                continue
            outs[fd].extend(chunk)
            size += len(chunk)
            if size > max_n:
                over = True
                live.clear()
                break
    return bytes(outs[proc.stdout.fileno()]), bytes(outs[proc.stderr.fileno()]), \
        False, over

def process_run(program, args, input_text, max_output, timeout_ms, k):
    argv = [str_out(program)]
    xs = args
    while xs["$"] == CID(Con):
        argv.append(str_out(xs["head"]))
        xs = xs["tail"]
    max_n = int(max_output)
    ms = int(timeout_ms)
    if max_n == 0 or ms == 0 or any("\0" in a for a in argv):
        return io_fail(22)
    try:
        proc = subprocess.Popen(argv, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
    except OSError as e:
        return io_fail(abs(e.errno) if e.errno else 5)
    deadline = time.monotonic() + ms / 1000
    try:
        proc.stdin.write(io_bytes(input_text))
        proc.stdin.close()
    except OSError:
        pass
    out_b, err_b, timed_out, over = _process_read(proc, max_n, deadline)
    if timed_out:
        proc.kill()
        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        return io_fail(errno.ETIMEDOUT)
    if over:
        proc.kill()
        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        return io_fail(27)
    try:
        proc.wait(timeout=max(0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        return io_fail(errno.ETIMEDOUT)
    code = proc.returncode
    code = 128 + (-code) if code < 0 else code
    return io_done(io_tup(code, io_text(out_b, len(out_b)), io_text(err_b, len(err_b))))

io_eff(CID(Process.run), process_run)
