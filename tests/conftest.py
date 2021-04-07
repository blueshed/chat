# pylint: disable=unused-argument
""" our test fixtures """
import logging
import urllib.parse
import pytest
import redis
import yaml
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from tornado.httpclient import HTTPRequest
from tornado.websocket import websocket_connect
from chat.main import make_app
from chat.redis_websocket import RedisWebsocket

log = logging.getLogger(__name__)


def init_db(sa_url, script_location):
    """ downgrade and upgrade db """
    url = sa_url.replace('mysql+aiomysql://', 'mysql+pymysql://')
    alembic_config = Config()
    alembic_config.set_main_option('sqlalchemy.url', url)
    alembic_config.set_main_option('script_location', script_location)
    command.downgrade(alembic_config, 'base')
    command.upgrade(alembic_config, 'head')
    log.info('db: upgrade')

    # load basic data
    engine = create_engine(url, future=True)
    with engine.connect() as conn:
        conn.execute(
            text(
                'insert into user (email, password) values ("dog1@test.com","dog1")'
            )
        )
        conn.commit()
    log.info('db: basic data')
    return sa_url


def init_redis(redis_url):
    """ tidy up before we start """
    conn = redis.from_url(redis_url)
    conn.flushall()
    conn.close()
    log.info('redis: flushed')


@pytest.fixture(name='settings', scope='session')
def load_settings():
    """ return our settings """
    with open('config/tests.yml') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope='module')
def test_db(settings):
    """ returns sqlalchemy engine """
    init_db(settings['sa']['url'], settings['sa_script_location'])
    return create_async_engine(settings['sa']['url'], echo=True, future=True)


@pytest.fixture
def app(settings, io_loop):
    """ return a tornado application """
    appl = make_app(settings)
    init_db(settings['sa']['url'], settings['sa_script_location'])
    if settings.get('redis'):
        init_redis(settings['redis']['redis_url'])
        io_loop.add_callback(
            RedisWebsocket.subscribe, appl, **settings['redis']
        )
    yield appl
    io_loop.run_sync(appl.settings['engine'].dispose)
    io_loop.run_sync(appl.settings['redis_pool'].close)


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
