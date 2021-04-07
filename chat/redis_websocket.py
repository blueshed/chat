# pylint: disable=W0201, W0221, W0236
""" We publish messages and subscribe to them """
import logging
import aioredis
from tornado.ioloop import IOLoop
from .websocket import Websocket

log = logging.getLogger(__name__)


class RedisWebsocket(Websocket):
    """ interrupt broadcast and send via redis topic """

    def initialize(self, topic_name, redis_url, **kwargs):
        """ allow some paths through """
        super().initialize(**kwargs)
        self.topic_name = topic_name
        self.redis_url = redis_url

    async def broadcast(self, message):
        """ publishes a document to topic """
        pool = self.settings['redis_pool']
        with await pool as conn:
            log.info('publish %s -> %r', self.topic_name, message)
            await conn.execute(
                'publish', self.topic_name, message.encode('utf-8')
            )

    @classmethod
    async def local_broadcast(cls, message):
        """ tell clients locally """
        for client in cls.clients:
            client.write_message(message)

    @classmethod
    async def subscribe(cls, app, topic_name, redis_url):
        """ run forever coroutine that listens to topic and broadcasts """

        try:
            redis = await aioredis.create_redis(redis_url)
            pool = await aioredis.create_pool(redis_url)
            app.settings['redis_pool'] = pool
            log.info('app.settings.redis_pool: %s', redis_url)
        except OSError as ex:
            log.exception(redis_url)
            if 'Connect call failed' in str(ex):
                log.warning('reconnecting redis: %s', ex)
                IOLoop.current().call_later(
                    0.1, cls.subscribe, topic_name, redis_url
                )
                return
            raise

        response = await redis.subscribe(topic_name)
        channel = response[0]
        log.info('subscribed to: %s', topic_name)
        try:
            while await channel.wait_message():
                message = await channel.get(encoding='utf-8')
                log.info('got document: %s', message)
                IOLoop.current().add_callback(cls.local_broadcast, message)
        except (GeneratorExit, StopAsyncIteration):
            log.info('redis subscription closing')
        except:
            log.exception('redis subscription')
            raise
        else:
            redis.close()
            await redis.wait_closed()
            log.exception('redis subscription closed')

    @classmethod
    async def unsubscribe(cls, app):
        """ closing pool """
        pool = app.settings['redis_pool']
        pool.close()
        await pool.wait_closed()
