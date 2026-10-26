from typing import Callable, Dict, Tuple
from ..http.request import Request
from ..http.response import Response

Handler = Callable[[Request], Response]

class Router:
    def __init__(self):
        self._routes: Dict[Tuple[str, str], Handler] = {}

    def route(self, method: str, path: str, handler: Handler) -> None:
        self._routes[(method.upper(), path)] = handler

    def dispatch(self, req: Request) -> Response:
        key = (req.method.upper(), req.path.split("?")[0])
        if key in self._routes:
            return self._routes[key](req)
        if req.path.startswith("/status/"):
            try:
                code = int(req.path.split("/")[-1])
                return Response(status=code, reason="Status")
            except ValueError:
                pass
        return Response(status=404, reason="Not Found",
                        headers={"Content-Type": "text/plain"}, body=b"404 Not Found")