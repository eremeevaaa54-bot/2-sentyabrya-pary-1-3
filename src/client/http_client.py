from typing import Dict, Optional
from ..http.parser import parse_response
from ..http.request import Request
from ..http.response import Response
from ..http.serializer import serialize_request
from ..http.url import Url
from ..net.tcp_client import TcpClient

class HttpError(Exception):
    def __init__(self, status: int, message: str = ""):
        self.status = status
        super().__init__(message or f"HTTP-ошибка {status}")

class HttpClient:
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Response:
        return self._request("GET", url, headers=headers)

    def post(self, url: str, body: bytes, content_type: str = "text/plain",
             headers: Optional[Dict[str, str]] = None) -> Response:
        headers = dict(headers or {})
        headers["Content-Type"] = content_type
        return self._request("POST", url, body=body, headers=headers)

    def _request(self, method: str, url: str, body: bytes = b"",
                 headers: Optional[Dict[str, str]] = None) -> Response:
        parsed = Url.parse(url)
        headers = dict(headers or {})
        headers.setdefault("Host", parsed.to_host_header())
        headers.setdefault("Connection", "close")
        headers.setdefault("User-Agent", "HttpGui/1.0")
        path = parsed.path
        if parsed.query:
            path = f"{path}?{parsed.query}"
        req = Request(method=method, path=path, headers=headers, body=body)
        raw = serialize_request(req)
        client = TcpClient(parsed.host, parsed.port, timeout=self.timeout, use_ssl=parsed.is_https)
        try:
            with client.connect() as sock:
                sock.send_all(raw)
                chunks = []
                while True:
                    data = sock.recv(65536)
                    if not data: break
                    chunks.append(data)
        finally:
            client.close()
        return parse_response(b"".join(chunks))