import inspect
import subprocess

# A child gets a pipe whose read end is closed as fd and writes a line
# there with the runtime's own io_out, read back through inspect.
# getsource, the way the JS twin embeds io_out's own source into its
# child. The answer is the child's status as a shell shows it: 128 plus
# the signal that ended it, else its exit code. resume names a C-only
# fork-and-resume-into-the-IO-loop case this backend has no process
# model for; the JS twin ignores it too, spawning a fresh interpreter
# either way, so this twin does the same.
def epipe_write(fd, resume, k):
    fd_i = int(fd)
    pr, pw = os.pipe()
    os.close(pr)
    code = ("import os, sys, signal\n"
        "signal.signal(signal.SIGPIPE, signal.SIG_DFL)\n"
        + inspect.getsource(io_out) + "\n"
        "io_out(" + str(fd_i) + ", b\"x\\n\")\n")
    kwargs = {"stdin": subprocess.DEVNULL}
    if fd_i == 1:
        kwargs["stdout"] = pw
    else:
        kwargs["stderr"] = pw
    r = subprocess.run([sys.executable, "-c", code], **kwargs, timeout=5)
    os.close(pw)
    return 128 - r.returncode if r.returncode < 0 else r.returncode

io_eff(CID(Epipe.write), epipe_write)
