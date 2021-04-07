"""
    Our entry point.

    Call: `python -m chat.main` with the following options:
    ::
            --cfg     config path (default config/dev.yml)
            --debug   auto reload (default False)
            --port    port to listen on (default 8080)
            --help    show this help information

    There are more logging options, see --help.
"""
import logging
import os
import yaml
from sqlalchemy.ext.asyncio import create_async_engine
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line
from .login import LoginHandler, LogoutHandler
from .websocket import Websocket
from .redis_websocket import RedisWebsocket
from .static_handler import AuthStaticFileHandler

log = logging.getLogger(__name__)

define('debug', type=bool, default=False, help='auto reload')
define('port', type=int, default=8080, help='port to listen on')
define('cfg', type=str, default='config/dev.yml', help='config path')


def make_app(settings):
    """ make a tornado application """
    if settings.get('redis'):
        ws_route = (r'/ws', RedisWebsocket, settings['redis'])
    else:
        ws_route = (r'/ws', Websocket)
    return Application(
        [
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            ws_route,
            (
                r'/docs/(.*)',
                StaticFileHandler,
                {'path': 'docs', 'default_filename': 'index.html'},
            ),
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
        engine=create_async_engine(**settings['sa']),
        **settings['tornado']
    )


def main():  # pragma nocover
    """ parse command line, make and start ioloop """
    parse_command_line()

    # load settings
    with open(options.cfg) as file:
        log.info('settings path: %s', options.cfg)
        settings = yaml.safe_load(file)

    # make app
    app = make_app(settings)
    port = int(os.getenv('PORT', options.port))
    app.listen(port)
    log.info('listening on port: %s', port)
    if options.debug:
        log.warning('running in debug mode')

    # start app
    ioloop = IOLoop.current()
    if settings.get('redis'):
        ioloop.add_callback(RedisWebsocket.subscribe, app, **settings['redis'])
    try:
        ioloop.start()
    except (KeyboardInterrupt, SystemExit):
        # graceful shutdown
        ioloop.run_sync(app.settings['engine'].dispose)
        if settings.get('redis'):
            ioloop.run_sync(app.settings['redis_pool'].close)
        ioloop.stop()


if __name__ == '__main__':
    main()  # pragma nocover
