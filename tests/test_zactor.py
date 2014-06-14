from pyczmq import zmq, zactor, zstr, zmsg, zsock

@zactor.callback
def echo_actor(pipe, args):
    assert args == "Hello, World"
    zsock.signal(pipe, 0)
    while True:
        msg = zmsg.recv(pipe)
        if not msg:
            break
        command = zmsg.popstr(msg)
        if command == "$TERM":
            return
        elif command == "ECHO":
            zmsg.send(msg, pipe)
        else:
            raise TypeError("E: invalid message to actor")


def test_zactor(verbose=False):
    actor = zactor.new(echo_actor, "Hello, World")
    zstr.sendx(actor, "ECHO", "This is a string")
    assert zstr.recv(actor) == "This is a string"

