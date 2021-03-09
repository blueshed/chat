# pylint: disable=unused-argument
""" our test fixtures """
import configparser
import urllib.parse
import os
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from tornado.httpclient import HTTPRequest
from tornado.websocket import websocket_connect
from chat.main import make_app


def init_db(settings):
    """ downgrade and upgrade db """
    db_url = settings['sa']['url']
    alembic_config = Config()
    alembic_config.set_main_option('sqlalchemy.url', db_url)
    alembic_config.set_main_option(
        'script_location', settings['sa_script_location']
    )
    if db_url.startswith('sqlite:///'):
        # sqlite does not like downgrading, zap it
        os.unlink(db_url[len('sqlite:///') :])
    else:
        command.downgrade(alembic_config, 'base')
    command.upgrade(alembic_config, 'head')

    # load basic data
    engine = create_engine(db_url)
    engine.execute(
        'insert into user (email, password) values ("dog1@test.com","dog1")'
    )
    return db_url


@pytest.fixture(name='settings', scope='session')
def load_settings():
    """ return our settings """
    config = configparser.ConfigParser()
    config.read('setup.cfg')
    section = config['testdb']
    return {
        'sa': {
            'url': section['sqlalchemy.url'],
            'echo': False,
            'future': True,
        },
        'sa_script_location': section['script_location'],
        'tornado': {
            'cookie_name': 'test-chat-cookie',
            'cookie_secret': 'test hat wearing',
            'login_url': '/login',
        },
    }


@pytest.fixture(scope='session')
def test_db(settings):
    """ returns sqlalchemy engine """
    db_url = init_db(settings)
    engine = create_engine(db_url, echo=True, future=True)
    return engine


@pytest.fixture
def app(settings):
    """ return a tornado application """
    return make_app(settings)


@pytest.fixture(name='cookie')
async def get_cookie(settings, http_server, http_server_client):
    """ login to get a cookie """
    response = await http_server_client.fetch(
        settings['tornado']['login_url'],
        headers={
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
        },
        method='POST',
        body=urllib.parse.urlencode(
            {'email': 'dog1@test.com', 'password': 'dog1', 'submit': 'login'}
        ),
        follow_redirects=False,
        raise_error=False,
    )
    print(response)
    return response.headers['Set-Cookie']


@pytest.fixture
async def ws_client(http_server, http_server_port):
    """ return a websocket client """
    request = HTTPRequest(f'ws://localhost:{http_server_port[1]}/ws')
    result = await websocket_connect(request)
    return result


@pytest.fixture
async def ws_auth_client(http_server, http_server_port, cookie):
    """ return a websocket client """
    request = HTTPRequest(
        f'ws://localhost:{http_server_port[1]}/ws',
        headers={'Cookie': await cookie},
    )
    result = await websocket_connect(request)
    return result


@pytest.fixture
async def ws_bad_client(http_server, http_server_port, cookie):
    """ return a websocket client """
    request = HTTPRequest(
        f'ws://localhost:{http_server_port[1]}/ws',
        headers={'Origin': 'http://locahost:3000', 'Cookie': await cookie},
    )
    result = await websocket_connect(request)
    return result
