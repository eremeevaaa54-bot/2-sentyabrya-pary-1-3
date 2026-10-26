import json
import logging
import threading
from ..http.parser import parse_request
from ..http.response import Response
from ..http.serializer import serialize_response
from ..http.url import ParseError
from ..net.socket_wrapper import Socket
from ..net.tcp_server import TcpServer
from .handlers import build_router
from .router import Router

logger = logging.getLogger(__name__)

class HttpServer:
    def __init__(self, port: int = 8080, log_callback=None):
        self.port = port
        self._tcp = TcpServer(port=port)
        self._tcp.set_handler(self._handle_client)
        self._router: Router = build_router()
        self._log_callback = log_callback
        self._lock = threading.Lock()

    def start(self) -> None:
        self._tcp.start()
        logger.info("Сервер запущен на порту %s", self.port)

    def stop(self) -> None:
        self._tcp.stop()
        logger.info("Сервер остановлен")

    def _handle_client(self, sock: Socket, addr: tuple) -> None:
        with self._lock:
            logger.info("Подключение от %s", addr)
        try:
            raw = self._read_full_request(sock)
        except Exception as exc:
            self._send(sock, Response(400, "Bad Request",
                                      headers={"Content-Type": "text/plain"},
                                      body=b"400 Bad Request"))
            return
        try:
            req = parse_request(raw)
        except ParseError:
            self._send(sock, Response(400, "Bad Request",
                                      headers={"Content-Type": "text/plain"},
                                      body=b"400 Bad Request"))
            return
        resp = self._router.dispatch(req)
        self._send(sock, resp)
        self._log(req, resp)

    @staticmethod
    def _read_full_request(sock: Socket) -> bytes:
        chunks = []
        while True:
            data = sock.recv(65536)
            if not data: break
            chunks.append(data)
            if b"\r\n\r\n" in b"".join(chunks): break
        return b"".join(chunks)

    @staticmethod
    def _send(sock: Socket, resp: Response) -> None:
        try: sock.send_all(serialize_response(resp))
        except OSError: pass

    def _log(self, req, resp: Response) -> None:
        from datetime import datetime
        record = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "method": req.method, "path": req.path,
            "status": resp.status, "length": len(resp.body),
        }
        logger.info("%s %s -> %s", req.method, req.path, resp.status)
        if self._log_callback:
            try: self._log_callback(json.dumps(record))
            except Exception: pass