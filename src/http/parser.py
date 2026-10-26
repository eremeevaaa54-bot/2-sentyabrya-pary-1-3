import re
from typing import Tuple
from .request import Request
from .response import Response
from .url import ParseError

MAX_HEADER_SIZE = 8192
STATUS_RE = re.compile(r"^HTTP/(?P<v>\d\.\d)\s+(?P<code>\d{3})\s*(?P<reason>.*)$")
REQUEST_LINE_RE = re.compile(r"^(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+HTTP/(?P<v>\d\.\d)$")

def _split_head_body(raw: bytes) -> Tuple[bytes, bytes]:
    idx = raw.find(b"\r\n\r\n")
    if idx == -1:
        raise ParseError("Не найдено окончание заголовков")
    return raw[:idx], raw[idx + 4:]

def _parse_headers(lines: list) -> dict:
    headers = {}
    if len(b"\r\n".join(lines)) > MAX_HEADER_SIZE:
        raise ParseError("Заголовки превышают 8 КБ")
    for line in lines:
        if not line: continue
        decoded = line.decode("iso-8859-1")
        if ":" not in decoded:
            raise ParseError(f"Неверная строка заголовка: {decoded!r}")
        name, _, value = decoded.partition(":")
        headers[name.strip()] = value.strip()
    return headers

def parse_request(raw: bytes) -> Request:
    head, body = _split_head_body(raw)
    lines = head.split(b"\r\n")
    if not lines: raise ParseError("Пустой запрос")
    request_line = lines[0].decode("iso-8859-1")
    match = REQUEST_LINE_RE.match(request_line)
    if not match:
        raise ParseError(f"Неверная стартовая строка: {request_line!r}")
    headers = _parse_headers(lines[1:])
    if "Host" not in headers and "host" not in {k.lower() for k in headers}:
        raise ParseError("Отсутствует Host")
    length = int(headers.get("Content-Length", 0) or 0)
    if len(body) < length:
        raise ParseError("Тело короче Content-Length")
    return Request(
        method=match.group("method"), path=match.group("path"),
        version=f"HTTP/{match.group('v')}", headers=headers, body=body[:length],
    )

def parse_response(raw: bytes) -> Response:
    head, body = _split_head_body(raw)
    lines = head.split(b"\r\n")
    if not lines: raise ParseError("Пустой ответ")
    status_line = lines[0].decode("iso-8859-1")
    match = STATUS_RE.match(status_line)
    if not match:
        raise ParseError(f"Неверная статус-строка: {status_line!r}")
    headers = _parse_headers(lines[1:])
    return Response(
        status=int(match.group("code")), reason=match.group("reason"),
        version=f"HTTP/{match.group('v')}", headers=headers, body=body,
    )