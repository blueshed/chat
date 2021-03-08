"""
    We need authenticated access to static files
"""
import urllib.parse
from urllib.parse import urlencode
from tornado.web import StaticFileHandler
from .login import UserMixin


class AuthStaticFileHandler(UserMixin, StaticFileHandler):
    """
    This provide integration between tornado.web.authenticated
    and tornado.web.StaticFileHandler.
    """

    def initialize(self, allow=None, **kwargs):  # pylint: disable=W0221
        """ allow some paths through """
        super().initialize(**kwargs)
        self.allow = allow if allow else []  # pylint: disable=W0201

    async def get(self, path, include_body=True):
        """ safe to return what you need """
        if self.current_user is None and path not in self.allow:
            return self.not_authenticated()
        return await StaticFileHandler.get(self, path, include_body)

    def not_authenticated(self):
        """ raise a redirect or error, tornado code dug out of a wrapper """
        url = self.get_login_url()
        if '?' not in url:
            if urllib.parse.urlsplit(url).scheme:
                # if login url is absolute, make next absolute too
                next_url = self.request.full_url()
            else:
                assert self.request.uri is not None
                next_url = self.request.uri
            url += '?' + urlencode(dict(next=next_url))
        self.redirect(url)
