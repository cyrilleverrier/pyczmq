import inspect
from pyczmq._cffi import C, ffi, ptop, cdef
from pyczmq import zmsg

__doc__ = """
"""

cdef('typedef struct _zsock_t zsock_t;')


@cdef('void zsock_destroy (zsock_t **p_self);')
def destroy(sock):
    """Destroy a sock."""
    C.zsock_destroy(ptop('zsock_t', sock))


@cdef('zsock_t * zsock_new (int type, const char *filename, size_t line_nbr);')
def new(type, filename=None, line_nbr=None):
    if filename is None:
        frame = inspect.stack()[1][0]
        info = inspect.getframeinfo(frame)
        filename = info.filename
        line_nbr = info.lineno
    return ffi.gc(C.zsock_new(type, filename, line_nbr), destroy)


@cdef('int zsock_bind (zsock_t *self, const char *format, ...);')
def bind(sock, endpoint):
    """ Bind a socket to a formatted endpoint. If the port is specified as '*'
    and the endpoint starts with "tcp://", binds to an ephemeral TCP port in
    a high range. Always returns the port number on successful TCP binds, else
    returns zero on success. Returns -1 on failure. When using ephemeral ports,
    note that ports may be reused by different threads, without clients being
    aware."""
    return C.zsock_bind(sock, endpoint)


@cdef('int zsock_unbind (zsock_t *self, const char *format, ...);')
def unbind(sock, endpoint):
    """Unbind a socket from a formatted endpoint.
    Returns 0 if OK, -1 if the endpoint was invalid or the function
    isn't supported."""
    return C.zsock_unbind(sock, endpoint)


@cdef('int zsock_connect (zsock_t *self, const char *format, ...);')
def connect(sock, endpoint):
    """Connect a socket to a formatted endpoint
    Returns 0 if OK, -1 if the endpoint was invalid."""
    return C.zsock_connect(sock, endpoint)


@cdef('int zsock_disconnect (zsock_t *self, const char *format, ...);')
def disconnect(sock, endpoint):
    """Disconnect a socket from a formatted endpoint
    Returns 0 if OK, -1 if the endpoint was invalid or the function
    isn't supported."""
    return C.zsock_disconnect(sock, endpoint)


@cdef('const char * zsock_type_str (zsock_t *self);')
def type_str(sock):
    """Returns socket type as printable constant string"""
    return ffi.string(C.zsock_type_str(sock))


@cdef('int zsock_send (zsock_t *self, zmsg_t **msg_p);')
def send(sock, msg):
    """Send a zmsg message to the socket, take ownership of the message
    and destroy when it has been sent.
    """
    return C.zsock_send(sock, ptop('zmsg_t', msg))


@cdef('zmsg_t * zsock_recv (zsock_t *self);')
def recv(sock):
    """Receive a zmsg message from the socket. Returns NULL if the process was
    interrupted before the message could be received, or if a receive timeout
    expired."""
    return C.zsock_recv(sock)


@cdef('int zsock_signal (void *self, unsigned char status);')
def signal(sock, status):
    """Send a signal over a socket. A signal is a short message carrying a
    success/failure code (by convention, 0 means OK). Signals are encoded
    to be distinguishable from "normal" messages. Accepts a zock_t or a
    zactor_t argument, and returns 0 if successful, -1 if the signal could
    not be sent."""
    return C.zsock_signal(sock, status)


@cdef('int zsock_wait (void *self);')
def wait(sock):
    """Wait on a signal. Use this to coordinate between threads, over pipe
    pairs. Blocks until the signal is received. Returns -1 on error, 0 or
    greater on success. Accepts a zsock_t or a zactor_t as argument."""
    return C.zsock_wait(sock)


@cdef('bool zsock_is (void *self);')
def zsock_is(sock):
    """Probe the supplied object, and report if it looks like a zsock_t."""
    return C.zsock_is(sock)


@cdef('void * zsock_resolve (void *self);')
def resolve(sock):
    """Probe the supplied reference. If it looks like a zsock_t instance,
    return the underlying libzmq socket handle; else if it looks like
    a libzmq socket handle, return the supplied value."""
    return C.zsock_resolve(sock)

cdef('void zsock_test (bool verbose);')
