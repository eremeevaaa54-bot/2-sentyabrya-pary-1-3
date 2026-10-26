import pytest
from src.http.parser import parse_request, parse_response
from src.http.url import ParseError

def test_parse_request_simple():
    raw = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    req = parse_request(raw)
    assert req.method == "GET"
    assert req.path == "/"

def test_parse_request_without_host_raises():
    raw = b"GET / HTTP/1.1\r\n\r\n"
    with pytest.raises(ParseError):
        parse_request(raw)

def test_parse_response_simple():
    raw = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nhi"
    resp = parse_response(raw)
    assert resp.status == 200
    assert resp.body == b"hi"