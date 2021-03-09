""" test websocket client """
import asyncio
from tornado.httpclient import HTTPClientError


async def test_ws(ws_client):
    """ test message send and receive """

    message = 'hello, world'

    client = await ws_client
    await client.write_message(message)
    response = await client.read_message()
    print(response)
    assert response == message

    client.close()
    await asyncio.sleep(0.01)


async def test_ws_cors_failure(ws_bad_client):
    """ test bad request """

    try:
        await ws_bad_client
        assert False, 'should have returned 403'
    except HTTPClientError as ex:
        assert ex.code == 403


async def test_ws_cors_success(ws_bad_client, app):
    """ test cors message send and receive """

    message = 'hello, world'
    app.settings['debug'] = True
    client = await ws_bad_client
    await client.write_message(message)
    response = await client.read_message()
    print(response)
    assert response == message

    client.close()
    await asyncio.sleep(0.01)
