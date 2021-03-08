""" test our user table """
from sqlalchemy import insert, select, update, delete
from chat.tables import user


def test_create(test_db):
    """ insert admin user """
    with test_db.connect() as conn:
        stmt = insert(user).values(email='admin@test.com', password='admin')
        result = conn.execute(stmt)
        conn.commit()
        assert result.inserted_primary_key[0] == 2

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
        stmt = update(user).where(user.c.id == result.id).values(profile={'foo': 'bar'})
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
