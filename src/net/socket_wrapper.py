import socket as _socket
from typing import Optional

class Socket:
    def __init__(self, sock: _socket.socket):
        self._sock: Optional[_socket.socket] = sock

    def __enter__(self) -> "Socket":
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self) -> None:
        try:
            if self._sock is not None:
                self._sock.close()
        finally:
            self._sock = None

    def send_all(self, data: bytes) -> None:
        assert self._sock is not None, "Сокет закрыт"
        self._sock.sendall(data)

    def recv(self, n: int) -> bytes:
        assert self._sock is not None, "Сокет закрыт"
        return self._sock.recv(n)

def create_tcp_socket() -> _socket.socket:
    return _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)