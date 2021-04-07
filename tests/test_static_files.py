""" test our static file handler """
import asyncio


async def test_favicon(http_server_client):
    """ can we get favicon without login """
    await asyncio.sleep(0.001)
    resp = await http_server_client.fetch('/favicon.ico')
    assert resp.code == 200


async def test_index_page(http_server_client, http_server_port, app):
    """ can we get favicon without login """
    await asyncio.sleep(0.001)
    resp = await http_server_client.fetch(
        '/', follow_redirects=False, raise_error=False
    )
    assert resp.code == 302

    app.settings['login_url'] = f'http://localhost:{http_server_port}/login'

    resp = await http_server_client.fetch(
        '/index.html', follow_redirects=False, raise_error=False
    )
    assert resp.code == 302

    app.settings['login_url'] = '/login'
