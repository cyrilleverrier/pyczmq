from pyczmq._cffi import C, ffi, ptop, cdef
from pyczmq import zsock, zmsg, zframe # need zsock_t, zmsg_t, zframe_t

__doc__ = """
"""


cdef('typedef struct _zactor_t zactor_t;')


# Actors get a pipe and arguments from caller
cdef('typedef void (zactor_fn) (zsock_t *pipe, void *args);')


def callback(f):
    @ffi.callback('zactor_fn')
    def handler(pipe, args):
        return f(pipe, ffi.from_handle(args))
    return handler


@cdef('void zactor_destroy (zactor_t **p_self);')
def destroy(actor):
    """Destroy an actor."""
    C.zactor_destroy(ptop('zactor_t', actor))


@cdef('zactor_t * zactor_new (zactor_fn *task, void *args);')
def new(task, args):
    """Create a new actor passing arbitrary arguments reference."""
    return ffi.gc(C.zactor_new(task, ffi.new_handle(args)), destroy)


@cdef('int zactor_send (zactor_t *self, zmsg_t **msg_p);')
def send(actor, msg):
    """Send a zmsg message to the actor, take ownership of the message
    and destroy when it has been sent."""
    return C.zactor_send(actor, msg)


@cdef('zmsg_t * zactor_recv (zactor_t *self);')
def recv(actor):
    """Receive a zmsg message from the actor. Returns NULL if the actor
    was interrupted before the message could be received, or if there
    was a timeout on the actor."""
    return C.zactor_recv(actor)


@cdef('bool zactor_is (void *self);')
def zactor_is(actor):
    """Probe the supplied object, and report if it looks like a zactor_t."""
    return C.zactor_is(actor)


@cdef('void * zactor_resolve (void *self);')
def resolve(actor):
    """Probe the supplied reference. If it looks like a zactor_t instance,
    return the underlying libzmq actor handle; else if it looks like
    a libzmq actor handle, return the supplied value."""
    return C.zactor_resolve(actor)


@cdef('void zactor_test (bool verbose);')
def test(verbose):
    """ Self test of this class """
    C.zactor_test(verbose)

