# Realtime Chat Persisted

<p align="center">
  <img alt="chat package" src="images/two-windows.png" width="1001">
</p>

This article is the third in the series [Realtime Chat with Vite, Vue3 and Python
Tornado](https://pspddo.medium.com/realtime-chat-with-vite-vue3-and-python-tornado-31c8085253af).
In this article we'd add SQLAlchemy persistence and authentication to our chat app.

So tooling up, we need to add [alembic](https://alembic.sqlalchemy.org/en/latest/)
to our `dev.txt` and [sqlalchemy](https://docs.sqlalchemy.org/en/14/) to our
`requirements.txt`. (NB. At the time of writing SQLAlchemy 1.4.0b3 was in beta
and so the actual entry in `requirements.txt` was `--pre sqlalchemy`).

Having done that, we can call `make setup` to install the new packages.

## SQLAlchemy

This package supports two flavours of persistence: an object relational mapper
and an expression language. We'll use the expression language. Create a
modules `chat/tables.py` and its contents:
```
""" our sqlalchemy schema """
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON


metadata = MetaData()


user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(128), nullable=False, unique=True),
    Column('password', String(60), nullable=False),
    Column('profile', JSON),
)
```


## Alembic

This package manages the migration of our database in response to changes in
our code. It is a tool used in setup and testing. It plays no part in runtime.
Not all databases support all of its features, but we'll avoid the obvious one,
such as removing a column from a table in sqlite. Alemic is a command line
tool and as such I'll need some additions to `tasks.py` to remember all the
syntax.

## tasks.py
```python
@task
def db_revise(ctx, message, name='chatdb', auto=False):
    """ create a revision """
    autogenerate = ' --autogenerate' if auto else ''
    ctx.run(f'alembic -c setup.cfg --name={name} revision -m {message!r}{autogenerate}')


@task
def db_upgrade(ctx, name='chatdb', revision='head'):
    """ upgrade db """
    ctx.run(f'alembic -c setup.cfg --name={name} upgrade {revision}')


@task
def db_downgrade(ctx, name='chatdb', revision='base'):
    """ downgrade db """
    ctx.run(f'alembic -c setup.cfg --name={name} downgrade {revision}')
```

These are the operations I perform and yet the tools is capable of so much
more. Please check out the documentation.

To begin we'll call `alembic init chat/scripts`. This will create a `scripts`
directory inside you `chat` package. Since it has no `__init__.py`, python will
not pick it up at runtime. Since projects can have many packages and this one
has a persistence layer, I see no reason to separate them. Alembic requires
two configuration parameters: the location of the scripts directory and the
sqlalchemy connection url to the database. This information is usually held
in the `alembic.ini`. We can dispose of it and put this information into our
`setup.cfg`:
```
[chatdb]
prepend_sys_path = .
script_location = chat/scripts
sqlalchemy.url = sqlite:///chat.db
```

Now we need to tell `alembic` where to find our `metadata`. Edit
`chat/scripts/env.py` and add this where `target_metadata` is defined:
```
import chat.tables

target_metadata = chat.tables.metadata
```

NB. Since our config provides no logging information you will need to comment
out line 14 - `#fileConfig(config.config_file_name)`. If we need to set
up logger we can do it later.

Now we can run our task: `inv db-revise -a -m 'first pass'` to autogenerate
a revision and `inv db-upgrade` to bring it up to date.

## Testing

Now test first and weep later - we need to test our database and our
SQLAlchemy table. To do this we'll need to create a test database that
uses alembic to prepare it. So lets first add to our `tests/conftest.py`:

```python
import configparser
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

def init_db(name='testdb'):
    """ downgrade and upgrade db """
    config = configparser.ConfigParser()
    config.read('setup.cfg')
    section = config[name]
    alembic_config = Config()
    alembic_config.set_main_option('sqlalchemy.url', section['sqlalchemy.url'])
    alembic_config.set_main_option(
        'script_location', section['script_location']
    )
    command.downgrade(alembic_config, 'base')
    command.upgrade(alembic_config, 'head')
    return section['sqlalchemy.url']


@pytest.fixture(scope='session')
def test_db():
    """ returns sqlalchemy engine """
    db_url = init_db()
    engine = create_engine(db_url, echo=True, future=True)
    return engine
```

We've stored our scripts and sqlalchemy.url in our `setup.cfg`. To
declare a test database we clone the settings and the `init_db` function
raids those settings to configure alembic. We `downgrade`, `upgrade` and
return the sqlalchemy.url. Then our fixture calls `init_db` and creates
our sqlalchemy engine. So how do we use this?

## tests/test_user.py
```python
""" test our user table """
from sqlalchemy import insert, select, update, delete
from chat.tables import user


def test_create(test_db):
    """ insert admin user """
    with test_db.connect() as conn:
        stmt = insert(user).values(email='admin@test.com', password='admin')
        result = conn.execute(stmt)
        conn.commit()
        assert result.inserted_primary_key[0] == 1

        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = conn.execute(stmt).first()
        assert result.email == 'admin@test.com'


def test_update(test_db):
    """ update admin user """
    with test_db.connect() as conn:
        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = conn.execute(stmt).first()
        print(result)
        assert result.email == 'admin@test.com'
        stmt = (
            update(user)
            .where(user.c.id == result.id)
            .values(profile={'foo': 'bar'})
        )
        result = conn.execute(stmt)
        assert result.rowcount == 1
        conn.commit()

        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = conn.execute(stmt).first()
        assert result.profile == {'foo': 'bar'}


def test_delete(test_db):
    """ let's delete admin """
    with test_db.connect() as conn:
        stmt = delete(user).where(user.c.email == 'admin@test.com')
        result = conn.execute(stmt)
        assert result.rowcount == 1
        conn.commit()

        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = conn.execute(stmt).first()
        assert result is None
```

Running our tests now, `inv test`, should produce and output:
```bash
---------- coverage: platform darwin, python 3.8.7-final-0 -----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
chat/__init__.py        0      0   100%
chat/main.py           11      0   100%
chat/tables.py          3      0   100%
chat/websocket.py      19      0   100%
-------------------------------------------------
TOTAL                  33      0   100%
```

We're ready for authentication!

## Authentication

Tornado has the scafolding for Authentication. We'll do a simple
local version and then point to the OAuth variations. Tornado
uses a secure cookie, so we'll need to add settings to our
Application instantiation.

    - cookie_name the name we'll use for our session cookie
    - cookie_secret the phase used to encrypt our cookie
    - login_url where to go to login

Since the command line would become too crowded with all these
options, now is a good to address configuration.

There are so many ways - we've aready used `setup.cfg`, but that is
for development. So let's create a top level directory called `config`
and create ourselves a `config/dev.yml` - not json as it does not
support comments well, not configparser as it does not support dictionaries.
The secret sauce to yml is `waddle` - a config package that support amazon
aws encryption so you can check in your settings and no one can get your
secrets. But that is too much for now, so this prepares for that step and
is simple to setup.

## config/dev.yml
```yml
---
# our settings for sqlalchemy.create_engine
sa:
    url: sqlite:///chat.db
    echo: False
    future: True

# our settings for tornado.we.Application
tornado:
    cookie_name: chat-user
    cookie_sectet: I do like your hat.
    login_url: /login
```

We'll adapt `chat/main.py`


We'll look at configuration later, but for now just add these
to `chat/main.py`:

```python
define('cfg', type=str, default='config/local.yml', help='config path')


def make_app(settings):
    """ make an application """
    engine = create_engine(**settings['sa'])
    return Application(
        [
            (r'/ws', Websocket),
            (r'/login', LoginHandler),
            (
                r'/(.*)',
                tornado.web.StaticFileHandler,
                {'path': 'chat/static', 'default_filename': 'index.html'},
            ),
        ],
        debug=options.debug,
        engine=engine,
        **settings['tornado']
    )


def main():  # pragma nocover
    """ parse command line, make and start """
    parse_command_line()

    with open(options.cfg) as file:
        settings = yaml.safe_load(file)

    app = make_app(settings)
```

Notice, we've added and option for our config file, we've added
settings as a parameter to `make_app`, we've added an `engine`
setting to our application and there is a mysterious `LoginHandler` -
we'll get there soon.

Loading our settings in main is a simple `safe_load`. But `make_app`
is also used in our `tests/conftest.py` - let's update that too:

## tests/conftest.py  - revisited
```python
def init_db(settings):
    """ downgrade and upgrade db """
    alembic_config = Config()
    alembic_config.set_main_option('sqlalchemy.url', settings['sa']['url'])
    alembic_config.set_main_option(
        'script_location', settings['sa_script_location']
    )
    command.downgrade(alembic_config, 'base')
    command.upgrade(alembic_config, 'head')
    return settings['sa']['url']


@pytest.fixture(name='settings', scope='session')
def load_settings():
    """ return our settings """
    config = configparser.ConfigParser()
    config.read('setup.cfg')
    section = config['testdb']
    return {
        'sa': {
            'url': section['sqlalchemy.url'],
            'echo': False,
            'future': True,
        },
        'sa_script_location': section['script_location'],
        'tornado': {
            'cookie_name': 'test-chat-cookie',
            'cookie_secret': 'test hat wearing',
            'login_url': '/login',
        },
    }


@pytest.fixture(scope='session')
def test_db(settings):
    """ returns sqlalchemy engine """
    db_url = init_db(settings)
    engine = create_engine(db_url, echo=True, future=True)
    return engine


@pytest.fixture
def app(settings):
    """ return a tornado application """
    return make_app(settings)
```

We've added a new fixture, `load_settings`, but we've given it a `name` attribute.
This is to not conflict the namespace and keep our linter from jumping up and
down at the bottom of the screen. As a parameter it is called `settings` and
pytest is clever enough to make this possible. Our app is using settings and
our test_db is using settings and settings is using `setup.cfg`. Our settings
have a non-production addition of the alembic script location - and our production
namespace is safe - no alembic.

So having done configuration we can write a login handler!

## login.py
``` python
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
            if email is None or password is None:
                raise HTTPError(403, 'email or password is None')
            user = None
            if submit == 'login':
                user = await self.login(email, password)
            if user:
                self.set_current_user(user)
                self.redirect(self.get_argument('next', '/'))
            else:
                raise Exception('email or password incorrect')
        except Exception as ex:  # pylint: disable=W0703
            log.exception(ex)
            self.get(error=str(ex))

    def set_current_user(self, value):
        """ put the current user in the cookie """
        if value:
            self.set_secure_cookie(self.cookie_name, json.dumps(value))
        else:
            self.clear_cookie(self.cookie_name)

    def login(self, email, password):
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
```

Now we need to users to test. We'll call `inv db-revise -m 'test data'` and
edit the generated file:
```python
def upgrade():
    """ setup test users """
    op.execute(
        "INSERT INTO user (email, password) VALUES ('dog1@test.com', 'dog1')"
    )
    op.execute(
        "INSERT INTO user (email, password) VALUES ('dog2@test.com', 'dog2')"
    )
```


The source is on [https://github.com/blueshed/chat/tree/persistence
](https://github.com/blueshed/chat/tree/persistence)
