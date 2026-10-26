import time
import pytest
from src.client.http_client import HttpClient
from src.server.http_server import HttpServer

@pytest.fixture()
def server():
    srv = HttpServer(port=18080)
    srv.start()
    time.sleep(0.1)  # ждем запуска
    yield srv
    srv.stop()

def test_get_root(server):
    resp = HttpClient().get("http://localhost:18080/")
    assert resp.status == 200
    assert b"Hello" in resp.body

def test_post_echo(server):
    resp = HttpClient().post("http://localhost:18080/echo", b"abc", "text/plain")
    assert resp.status == 200
    assert resp.body == b"abc"

def test_status_404(server):
    assert HttpClient().get("http://localhost:18080/status/404").status == 404