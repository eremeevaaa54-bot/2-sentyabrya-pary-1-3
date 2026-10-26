import socket
import threading
from typing import Callable, Optional
from .socket_wrapper import Socket, create_tcp_socket

class TcpServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8080, backlog: int = 5):
        self.host = host
        self.port = port
        self.backlog = backlog
        self._raw: Optional[socket.socket] = None
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._handler: Optional[Callable[[Socket, tuple], None]] = None

    def set_handler(self, handler: Callable[[Socket, tuple], None]) -> None:
        self._handler = handler

    def start(self) -> None:
        raw = create_tcp_socket()
        raw.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw.bind((self.host, self.port))
        raw.listen(self.backlog)
        raw.settimeout(0.5)
        self._raw = raw
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._serve_forever, daemon=True)
        self._thread.start()

    def _serve_forever(self) -> None:
        assert self._raw is not None
        while not self._stop_event.is_set():
            try:
                conn, addr = self._raw.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with Socket(conn) as sock:
                if self._handler:
                    try:
                        self._handler(sock, addr)
                    except Exception:
                        pass

    def stop(self) -> None:
        self._stop_event.set()
        if self._raw:
            try: self._raw.close()
            finally: self._raw = None
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None