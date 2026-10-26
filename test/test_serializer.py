from src.http.request import Request
from src.http.response import Response
from src.http.serializer import serialize_request, serialize_response

def test_serialize_request_ends_with_crlf_crlf():
    raw = serialize_request(Request(method="GET", path="/", headers={"Host": "x"}))
    assert raw.endswith(b"\r\n\r\n")

def test_serialize_response_has_content_length():
    raw = serialize_response(Response(status=200, reason="OK", body=b"hello"))
    assert b"Content-Length: 5" in raw