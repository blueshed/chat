""" our entry point """
import logging
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from .websocket import Websocket

log = logging.getLogger(__name__)

define('debug', type=bool, default=False, help='auto reload')
define('port', type=int, default=8080, help='port to listen on')


def make_app():
    """ make an application """
    return tornado.web.Application(
        [
            (r'/ws', Websocket),
            (
                r'/(.*)',
                tornado.web.StaticFileHandler,
                {'path': 'chat/static', 'default_filename': 'index.html'},
            ),
        ],
        debug=options.debug,
    )


def main():
    """ parse command line, make and start """
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    log.info('listening on port: %s', options.port)
    if options.debug:
        log.warning('running in debug mode')
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
