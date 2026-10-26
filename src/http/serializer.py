from .request import Request
from .response import Response

CRLF = "\r\n"

def _build_start_line(line: str, headers: dict, body: bytes) -> bytes:
    headers = dict(headers)
    if "Content-Length" not in {k.lower() for k in headers} and body:
        headers["Content-Length"] = str(len(body))
    parts = [line]
    for key, value in headers.items():
        parts.append(f"{key}: {value}")
    parts.append("")
    parts.append("")
    return CRLF.join(parts).encode("iso-8859-1") + body

def serialize_request(req: Request) -> bytes:
    start = f"{req.method} {req.path} {req.version}"
    return _build_start_line(start, req.headers, req.body)

def serialize_response(resp: Response) -> bytes:
    reason = resp.reason or ""
    start = f"{resp.version} {resp.status} {reason}".strip()
    headers = dict(resp.headers)
    lower = {k.lower() for k in headers}
    if "content-length" not in lower:
        headers["Content-Length"] = str(len(resp.body))
    if "content-type" not in lower and resp.body:
        headers["Content-Type"] = "text/plain; charset=utf-8"
    return _build_start_line(start, headers, resp.body)