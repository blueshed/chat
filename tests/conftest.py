""" our test fictures """
import pytest
from tornado.httpclient import HTTPRequest
from tornado.websocket import websocket_connect
from chat.main import make_app


@pytest.fixture
def app():
    """ return a tornado application """
    return make_app()


@pytest.fixture
async def ws_client(http_server, http_server_port):
    """ return a websocket client """
    request = HTTPRequest(f'ws://localhost:{http_server_port[1]}/ws')
    result = await websocket_connect(request)
    return result


@pytest.fixture
async def ws_bad_client(http_server, http_server_port):
    """ return a websocket client """
    request = HTTPRequest(
        f'ws://localhost:{http_server_port[1]}/ws',
        headers={'Origin': 'http://locahost:3000'},
    )
    result = await websocket_connect(request)
    return result
