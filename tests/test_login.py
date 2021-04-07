""" test our login and logout handler """
import asyncio
import urllib.parse


async def test_login_get(http_server_client):
    """ can we get favicon without login """
    await asyncio.sleep(0.001)
    resp = await http_server_client.fetch('/login')
    assert resp.code == 200


async def test_logout(http_server_client, cookie):
    """ can we get favicon without login """
    await asyncio.sleep(0.001)
    resp = await http_server_client.fetch(
        '/logout',
        headers={'Cookie': await cookie},
        follow_redirects=False,
        raise_error=False,
    )
    assert resp.code == 302


async def fetch(client, body):
    """ helper """
    await asyncio.sleep(0.001)
    return await client.fetch(
        '/login',
        headers={
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
        },
        method='POST',
        body=urllib.parse.urlencode(body),
        follow_redirects=False,
        raise_error=False,
    )


async def test_login_errors(http_server_client):
    """ what if we pass in a wrong password or no email """
    await asyncio.sleep(0.001)
    response = await fetch(
        http_server_client,
        {'email': 'dog1@test.com', 'password': 'dog2', 'submit': 'login'},
    )
    print(response.body)
    assert b'email or password incorrect' in response.body

    response = await fetch(
        http_server_client,
        {'email': 'dog1@test.com', 'password': '', 'submit': 'login'},
    )
    print(response.body)
    assert b'email or password is None' in response.body

    response = await fetch(
        http_server_client, {'email': 'dog1@test.com', 'submit': 'login'},
    )
    print(response.body)
    assert b'email or password is None' in response.body
