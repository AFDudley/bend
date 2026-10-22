# Process
# =======

import subprocess

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
    try:
        out_b, err_b = proc.communicate(input=io_bytes(input_text),
            timeout=ms / 1000)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return io_fail(5)
    if len(out_b) + len(err_b) > max_n:
        return io_fail(27)
    code = proc.returncode
    code = 128 + (-code) if code < 0 else code
    return io_done(io_tup(code, io_text(out_b, len(out_b)), io_text(err_b, len(err_b))))

io_eff(CID(Process.run), process_run)
