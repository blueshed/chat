# pylint: disable=W0201, W0221, W0236
""" our websocket handler """
import json
import logging
from tornado.websocket import WebSocketHandler
from .login import UserMixin

log = logging.getLogger(__name__)


class Websocket(UserMixin, WebSocketHandler):
    """ a websocket handler that broadcasts to all clients """

    clients = []

    def check_origin(self, origin):
        """ in development allow ws from anywhere """
        if self.settings.get('debug', False):
            return True
        return super().check_origin(origin)

    def open(self, *args, **kwargs):
        """ we connected """
        if self.current_user is None:
            self.close(401, 'not authenticated')
            return
        email = self.current_user['email']
        log.info('WebSocket opened: %s', email)
        self.write_message(email)
        self.clients.append(self)

    def on_close(self):
        """ we're done """
        if self in self.clients:
            self.clients.remove(self)
        log.info('WebSocket closed')

    async def on_message(self, message):
        """ we've said something, tell everyone """
        email = self.current_user['email']
        message = json.dumps({'user': email, 'message': message})
        await self.broadcast(message)

    async def broadcast(self, message):
        """ send a message to all clients """
        for client in self.clients:
            client.write_message(message)
