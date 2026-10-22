import subprocess
import inspect

# A host zero-byte standard-stream write fails instead of retrying
# forever. The child runs the runtime's own io_out, read back from this
# file through inspect.getsource, the way the JS twin embeds io_out's own
# source into its child.
def stream_write_zero(k):
    for fd in (1, 2):
        code = ("import os, sys, signal\n"
            + inspect.getsource(io_out) + "\n"
            "real_write = os.write\n"
            "def stalled_write(f, data):\n"
            "    return 0 if f == " + str(fd) + " and len(data) > 0 "
            "else real_write(f, data)\n"
            "os.write = stalled_write\n"
            "io_out(" + str(fd) + ", b\"x\")\n")
        r = subprocess.run([sys.executable, "-c", code],
            capture_output=True, text=True, timeout=2)
        want_err = "bend: a short write on a standard stream\n" if fd == 1 else ""
        if r.returncode != 1 or r.stdout != "" or r.stderr != want_err:
            return fd
    return 0

io_eff(CID(Stream.write_zero), stream_write_zero)
