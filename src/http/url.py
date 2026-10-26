from dataclasses import dataclass, field
from typing import Dict
from urllib.parse import parse_qs, urlparse

class ParseError(Exception):
    pass

@dataclass
class Url:
    scheme: str
    host: str
    port: int
    path: str
    query: str = ""
    query_params: Dict[str, list] = field(default_factory=dict)

    @classmethod
    def parse(cls, raw: str) -> "Url":
        if not raw or not isinstance(raw, str):
            raise ParseError(f"Пустой или неверный URL: {raw!r}")
        parsed = urlparse(raw.strip())
        if parsed.scheme not in ("http", "https"):
            raise ParseError(f"Неподдерживаемая схема: {parsed.scheme!r}")
        if not parsed.hostname:
            raise ParseError(f"Не указан хост в URL: {raw!r}")
        try:
            port = parsed.port
        except ValueError as exc:
            raise ParseError(f"Неверный порт: {exc}") from exc
        if port is None:
            port = 443 if parsed.scheme == "https" else 80
        path = parsed.path or "/"
        query = parsed.query or ""
        return cls(
            scheme=parsed.scheme, host=parsed.hostname, port=port,
            path=path, query=query, query_params=parse_qs(query),
        )

    @property
    def is_https(self) -> bool:
        return self.scheme == "https"

    def to_host_header(self) -> str:
        default = 443 if self.is_https else 80
        if self.port == default:
            return self.host
        return f"{self.host}:{self.port}"