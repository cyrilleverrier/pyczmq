from pyczmq import zmq, zsock, zstr

def test_zsock(verbose=False):
    writer = zsock.new(zmq.PUSH)
    reader = zsock.new(zmq.PULL)
    assert zsock.type_str(writer) == 'PUSH'
    assert zsock.type_str(reader) == 'PULL'
    zsock.bind(writer, 'inproc://foo')
    zsock.connect(reader, 'inproc://foo')
    zstr.send(writer, "hello!")
    assert zstr.recv(reader) == 'hello!'

