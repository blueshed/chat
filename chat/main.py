""" our entry point """
import logging
import tornado.ioloop
import yaml
from sqlalchemy import create_engine
from tornado.web import Application
from tornado.options import define, options, parse_command_line
from .login import LoginHandler, LogoutHandler
from .websocket import Websocket
from .static_handler import AuthStaticFileHandler

log = logging.getLogger(__name__)

define('debug', type=bool, default=False, help='auto reload')
define('port', type=int, default=8080, help='port to listen on')
define('cfg', type=str, default='config/dev.yml', help='config path')


def make_app(settings):
    """ make an application """
    engine = create_engine(**settings['sa'])
    return Application(
        [
            (r'/ws', Websocket),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (
                r'/(.*)',
                AuthStaticFileHandler,
                {
                    'path': 'chat/static',
                    'default_filename': 'index.html',
                    'allow': ['favicon.ico'],
                },
            ),
        ],
        debug=options.debug,
        engine=engine,
        **settings['tornado']
    )


def main():  # pragma nocover
    """ parse command line, make and start """
    parse_command_line()

    # load settings
    with open(options.cfg) as file:
        log.info('settings path: %s', options.cfg)
        settings = yaml.safe_load(file)

    # make app
    app = make_app(settings)
    app.listen(options.port)
    log.info('listening on port: %s', options.port)
    if options.debug:
        log.warning('running in debug mode')

    # start app
    ioloop = tornado.ioloop.IOLoop.current()
    try:
        ioloop.start()
    except (KeyboardInterrupt, SystemExit):
        # graceful shutdown
        ioloop.stop()


if __name__ == '__main__':
    main()  # pragma nocover
