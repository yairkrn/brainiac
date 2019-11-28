import socket


class Connection:
    def __init__(self, socket):
        self._socket = socket

    def __repr__(self):
        peer_address = '{}:{}'.format(*self._socket.getpeername())
        sock_address = '{}:{}'.format(*self._socket.getsockname())
        return f'<Connection from {sock_address} to {peer_address}>'

    def send(self, data):
        self._socket.sendall(data)

    def receive(self, size):
        data = bytes()
        while len(data) < size:
            data_chunk = self._socket.recv(size - len(data))
            if data_chunk == b'':
                raise RuntimeError('Connection aborted! %d / %d bytes received'.format(len(data), size))
            data += (data_chunk)
        return data  

    def close(self):
        self._socket.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
