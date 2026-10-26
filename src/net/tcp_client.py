import socket
import ssl
from typing import Optional
from .socket_wrapper import Socket, create_tcp_socket

class ConnectionError_(Exception): pass
class TimeoutError_(Exception): pass

class TcpClient:
    def __init__(self, host: str, port: int, timeout: float = 5.0, use_ssl: bool = False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.use_ssl = use_ssl
        self._sock: Optional[Socket] = None

    def connect(self) -> Socket:
        raw = create_tcp_socket()
        raw.settimeout(self.timeout)
        try:
            raw.connect((self.host, self.port))
        except socket.timeout as exc:
            raw.close()
            raise TimeoutError_(f"Таймаут: {self.host}:{self.port}") from exc
        except OSError as exc:
            raw.close()
            raise ConnectionError_(f"Не удалось подключиться: {exc}") from exc
        if self.use_ssl:
            ctx = ssl.create_default_context()
            try:
                raw = ctx.wrap_socket(raw, server_hostname=self.host)
            except ssl.SSLError as exc:
                raw.close()
                raise ConnectionError_(f"SSL-ошибка: {exc}") from exc
        self._sock = Socket(raw)
        return self._sock

    def close(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None