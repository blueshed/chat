""" our websocket handler """
import logging
from tornado.websocket import WebSocketHandler

log = logging.getLogger(__name__)


class Websocket(WebSocketHandler):
    """ a websocket handler that broadcasts to all clients """

    clients = []

    def check_origin(self, origin):
        """ in development allow ws from anywhere """
        if self.settings.get('debug', False):
            return True
        return super().check_origin(origin)

    def open(self, *args, **kwargs):
        """ we connected """
        log.info('WebSocket opened')
        self.clients.append(self)

    def on_close(self):
        """ we're done """
        if self in self.clients:
            self.clients.remove(self)
        log.info('WebSocket closed')

    def on_message(self, message):
        """ we've said something, tell everyone """
        for client in self.clients:
            client.write_message(message)
