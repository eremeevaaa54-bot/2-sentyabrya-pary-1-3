import json
import time
from datetime import datetime
from ..http.request import Request
from ..http.response import Response

def echo_get(req: Request) -> Response:
    return Response(status=200, reason="OK",
                    headers={"Content-Type": "text/html; charset=utf-8"},
                    body=b"<h1>Hello</h1>")

def echo_post(req: Request) -> Response:
    ctype = req.header("Content-Type", "text/plain")
    return Response(status=200, reason="OK",
                    headers={"Content-Type": ctype}, body=req.body)

def time_get(req: Request) -> Response:
    body = json.dumps({"time": datetime.now().isoformat(),
                       "timestamp": time.time()}).encode()
    return Response(status=200, reason="OK",
                    headers={"Content-Type": "application/json"}, body=body)

def headers_get(req: Request) -> Response:
    body = json.dumps(dict(req.headers)).encode()
    return Response(status=200, reason="OK",
                    headers={"Content-Type": "application/json"}, body=body)

def build_router():
    from .router import Router
    router = Router()
    router.route("GET", "/", echo_get)
    router.route("GET", "/echo", echo_get)
    router.route("POST", "/echo", echo_post)
    router.route("GET", "/time", time_get)
    router.route("GET", "/headers", headers_get)
    return router