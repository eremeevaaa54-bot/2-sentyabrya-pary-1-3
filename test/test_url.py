import pytest
from src.http.url import ParseError, Url

def test_parse_with_port_and_query():
    u = Url.parse("http://host:8080/path?q=1")
    assert u.host == "host"
    assert u.port == 8080
    assert u.path == "/path"

def test_parse_default_port_80():
    u = Url.parse("http://host/path")
    assert u.port == 80

def test_parse_garbage_raises():
    with pytest.raises(ParseError):
        Url.parse("garbage")