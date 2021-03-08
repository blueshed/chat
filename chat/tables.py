""" our sqlalchemy schema """
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON


metadata = MetaData()


user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(128), nullable=False, unique=True),
    Column('password', String(60), nullable=False),
    Column('profile', JSON, default={}),
)
