""" our entry point """
import logging
import tornado.ioloop
from tornado.web import Application
from tornado.options import define, options, parse_command_line
from .websocket import Websocket

log = logging.getLogger(__name__)

define('debug', type=bool, default=False, help='auto reload')
define('port', type=int, default=8080, help='port to listen on')


def make_app():
    """ make an application """
    return Application(
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


def main():  # pragma nocover
    """ parse command line, make and start """
    parse_command_line()
    app = make_app()
    app.listen(options.port)
    log.info('listening on port: %s', options.port)
    if options.debug:
        log.warning('running in debug mode')
    ioloop = tornado.ioloop.IOLoop.current()
    try:
        ioloop.start()
    except (KeyboardInterrupt, SystemExit):
        # graceful shutdown
        ioloop.stop()


if __name__ == '__main__':
    main()  # pragma nocover
