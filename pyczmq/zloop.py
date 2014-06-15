from pyczmq._cffi import ffi, C, ptop, cdef
from pyczmq import zsock

__doc__ = """
The zloop class provides an event-driven reactor pattern. The reactor
handles zmq_pollitem_t items (pollers or writers, sockets or fds), and
once-off or repeated timers. Its resolution is 1 msec. It uses a
tickless timer to reduce CPU interrupts in inactive processes.
"""


cdef('typedef struct _zloop_t zloop_t;')
cdef('typedef int (zloop_fn) (zloop_t *loop, zmq_pollitem_t *item, void *arg);')
cdef('typedef int (zloop_timer_fn) (zloop_t *loop, int timer_id, void *arg);')
cdef('typedef int (zloop_reader_fn) (zloop_t *loop, zsock_t *reader, void *arg);')


def poll_callback(f):
    @ffi.callback('zloop_fn')
    def handler(loop, item, arg):
        return f(loop, item, ffi.from_handle(arg))
    return handler


def timer_callback(f):
    @ffi.callback('zloop_timer_fn')
    def handler(loop, timer_id, arg):
        return f(loop, timer_id, ffi.from_handle(arg))
    return handler


def reader_callback(f):
    @ffi.callback('zloop_reader_fn')
    def handler(loop, reader, arg):
        return f(loop, reader, ffi.from_handle(arg))
    return handler


# old generic name before timers and readers
callback = poll_callback


@cdef('int zloop_reader (zloop_t *self, zsock_t *sock, zloop_reader_fn handler, void *arg);')
def reader(loop, sock, handler, arg):
    """Register socket reader with the reactor. When the reader has messages,
    the reactor will call the handler, passing the arg. Returns 0 if OK, -1
    if there was an error. If you register the same socket more than once,
    each instance will invoke its corresponding handler."""
    return C.zloop_reader(loop, sock, handler, ffi.new_handle(arg))


@cdef('void zloop_reader_end (zloop_t *self, zsock_t *sock);')
def reader_end(loop, sock):
    """Cancel a socket reader from the reactor. If multiple readers exist for
    same socket, cancels ALL of them."""
    return C.zloop_reader_end(loop, sock)


@cdef('void zloop_reader_set_tolerant (zloop_t *self, zsock_t *sock);')
def reader_set_tolerant(loop, sock):
    """Configure a registered reader to ignore errors. If you do not set this,
    then readers that have errors are removed from the reactor silently."""
    return C.zloop_reader_set_tolerant(loop, sock)


@cdef('void zloop_destroy (zloop_t **self_p);')
def destroy(loop):
    """
    Destroy a reactor, this is not necessary if you create it with
    new.
    """
    C.zloop_destroy(ptop('zloop_t', loop))


@cdef(' zloop_t * zloop_new (void);')
def new():
    """Create a new zloop reactor"""
    return ffi.gc(C.zloop_new(), destroy)


@cdef('int zloop_poller (zloop_t *self, zmq_pollitem_t *item,'
         ' zloop_fn handler, void *arg);')
def poller(p, item, handler, arg=None):
    """
    Register pollitem with the reactor. When the pollitem is ready, will call
    the handler, passing the arg. Returns 0 if OK, -1 if there was an error.
    If you register the pollitem more than once, each instance will invoke its
    corresponding handler.

    """
    return C.zloop_poller(p, item, handler, ffi.new_handle(arg))


@cdef('void zloop_poller_end (zloop_t *self, zmq_pollitem_t *item);')
def poller_end(loop, item):
    """
    Cancel a pollitem from the reactor, specified by socket or FD. If both
    are specified, uses only socket. If multiple poll items exist for same
    socket/FD, cancels ALL of them.
    """
    return C.zloop_poller_end(loop, item)


@cdef('void zloop_poller_set_tolerant (zloop_t *self, zmq_pollitem_t *item);')
def poller_set_tolerant(loop, item):
    """
    Configure a registered pollitem to ignore errors. If you do not set this,
    then pollitems that have errors are removed from the reactor silently.
    """
    return C.zloop_poller_set_tolerant(loop, item)


@cdef('int zloop_timer (zloop_t *self, size_t delay, size_t times, zloop_timer_fn handler, void *arg);')
def timer(loop, delay, times, handler, arg):
    """
    Register a timer that expires after some delay and repeats some number of
    times. At each expiry, will call the handler, passing the arg. To
    run a timer forever, use 0 times. Returns a timer_id or -1 if there was an
    error.
    """
    return C.zloop_timer(loop, delay, times, handler, ffi.new_handle(arg))


@cdef('int zloop_timer_end (zloop_t *self, int timer_id);')
def timer_end(loop, arg):
    """
    Cancel a specific timer (as provided by zloop_timer)
    """
    return C.zloop_timer_end(loop, arg)


@cdef('void zloop_set_verbose (zloop_t *self, bool verbose);')
def set_verbose(loop, verbose):
    """
    Set verbose tracing of reactor on/off
    """
    return C.zloop_set_verbose(loop, verbose)


@cdef('int zloop_start (zloop_t *self);')
def start(loop):
    """
    Start the reactor. Takes control of the thread and returns when the 0MQ
    context is terminated or the process is interrupted, or any event handler
    returns -1. Event handlers may register new sockets and timers, and
    cancel sockets. Returns 0 if interrupted, -1 if cancelled by a handler.
    """
    return C.zloop_start(loop)


cdef('void zloop_test (bool verbose);')

