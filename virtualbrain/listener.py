from connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self._host = host
        self._port = port
        self._backlog = backlog
        self._reuseaddr = reuseaddr

        self._socket = socket.socket()

        if reuseaddr:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self._socket.bind((host, port))
        
    @property
    def host(self):
        return self._host
        
    @property
    def port(self):
        return self._port
    
    @property
    def backlog(self):
        return self._backlog

    @property
    def reuseaddr(self):
        return self._reuseaddr

    def __repr__(self):
        return f'Listener(port={self._port}, host=\'{self._host}\', backlog={self._backlog}, reuseaddr={self._reuseaddr})'
    
    def start(self):
        self._socket.listen(self._backlog)

    def stop(self):
        self._socket.close()

    def accept(self):
        client, address = self._socket.accept()
        return Connection(client)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()
