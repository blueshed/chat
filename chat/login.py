""" our login handler """
import json
import logging
from sqlalchemy import select
from tornado.web import RequestHandler, HTTPError
from . import tables

log = logging.getLogger(__name__)


class UserMixin:
    """ for use by authenticated handlers """

    @property
    def cookie_name(self):
        """ return the cookie_name declared in application settings"""
        return self.settings.get('cookie_name')

    def get_current_user(self):
        """ return the current user from the cookie """
        result = self.get_secure_cookie(self.cookie_name)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result


class LoginHandler(UserMixin, RequestHandler):
    """ handle login get and post """

    def get(self, error=None):
        """ render the form """
        email = self.get_argument('email', default=None)
        next_ = self.get_argument('next', '/')
        self.render(
            'login.html', email=email, error=error, next=next_,
        )

    async def post(self):
        """ handle login post """
        try:
            email = self.get_argument('email', None)
            password = self.get_argument('password', None)
            submit = self.get_argument('submit', 'login')
            if not email or not password:
                raise HTTPError(403, 'email or password is None')
            user = None
            if submit == 'login':
                user = await self.login(email, password)
            if user:
                self.set_secure_cookie(self.cookie_name, json.dumps(user))
                self.redirect(self.get_argument('next', '/'))
            else:
                raise Exception('email or password incorrect')
        except Exception as ex:  # pylint: disable=W0703
            log.exception(ex)
            self.get(error=str(ex))

    async def login(self, email, password):
        """ can we login ? """
        user = None
        engine = self.settings['engine']
        with engine.connect() as conn:
            stmt = select(tables.user).where(
                tables.user.c.email == email, tables.user.c.password == password,
            )
            row = conn.execute(stmt).first()
            if row:
                user = {'id': row.id, 'email': row.email}
        return user


class LogoutHandler(UserMixin, RequestHandler):
    """
    removes the cookie defined in application settings
    and redirects.
    """

    def get(self):
        """ removes cookie and redirects to optional next argument """
        self.clear_cookie(self.cookie_name)
        self.redirect(self.get_argument('next', '/login'))
