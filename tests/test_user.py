""" test our user table """
from sqlalchemy import insert, select, update, delete
from chat.tables import user


async def test_create(test_db):
    """ insert admin user """
    async with test_db.connect() as conn:
        stmt = insert(user).values(email='admin@test.com', password='admin')
        result = await conn.execute(stmt)
        await conn.commit()
        assert result.inserted_primary_key[0] == 2

        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = await conn.execute(stmt)
        assert result.first().email == 'admin@test.com'


async def test_update(test_db):
    """ update admin user """
    async with test_db.connect() as conn:
        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = await conn.execute(stmt)
        result = result.first()
        print(result)
        assert result.email == 'admin@test.com'
        stmt = update(user).where(user.c.id == result.id).values(profile={'foo': 'bar'})
        result = await conn.execute(stmt)
        assert result.rowcount == 1
        await conn.commit()

        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = await conn.execute(stmt)
        assert result.first().profile == {'foo': 'bar'}


async def test_delete(test_db):
    """ let's delete admin """
    async with test_db.connect() as conn:
        stmt = delete(user).where(user.c.email == 'admin@test.com')
        result = await conn.execute(stmt)
        assert result.rowcount == 1
        await conn.commit()

        stmt = select(user).where(user.c.email == 'admin@test.com')
        result = await conn.execute(stmt)
        assert result.first() is None
