""" test websocket client """
import asyncio
import json
import logging
from tornado.httpclient import HTTPClientError


async def test_no_auth_ws(ws_client):
    """ test we need to authenticate """
    await asyncio.sleep(0.001)
    client = await ws_client
    response = await client.read_message()
    assert response is None, 'nothing to read - is closed'


async def test_ws(ws_auth_client, caplog):
    """ test message send and receive """
    await asyncio.sleep(0.001)
    message = 'hello, world'
    with caplog.at_level(logging.DEBUG):
        client = await ws_auth_client
        await asyncio.sleep(0.01)
        response = await client.read_message()
        assert response == 'dog1@test.com'
        await client.write_message(message)
        assert False
        response = await client.read_message()
        print(response)
        assert response == json.dumps(
            {'user': 'dog1@test.com', 'message': message}
        )
        client.close()


async def test_ws_cors_failure(ws_bad_client):
    """ test message send and receive """
    await asyncio.sleep(0.001)
    try:
        await ws_bad_client
        assert False, 'should have returned 403'
    except HTTPClientError as ex:
        assert ex.code == 403


async def test_ws_cors_success(ws_bad_client, app):
    """ test message send and receive """
    await asyncio.sleep(0.001)
    
    message = 'hello, world'
    app.settings['debug'] = True
    client = await ws_bad_client
    await asyncio.sleep(0.01)

    response = await client.read_message()
    assert response == 'dog1@test.com'
    await client.write_message(message)
    response = await client.read_message()
    print(response)
    assert response == json.dumps(
        {'user': 'dog1@test.com', 'message': message}
    )

    client.close()
