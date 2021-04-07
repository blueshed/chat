""" test our redis """
import aioredis


async def test_ws(settings):
    """ test redis get """
    if settings.get('redis'):
        redis = await aioredis.create_redis_pool(
            settings['redis']['redis_url']
        )
        await redis.set('my-key', 'value')
        val = await redis.get('my-key', encoding='utf-8')
        assert val == 'value'
        redis.close()
        await redis.wait_closed()
