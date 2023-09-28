from sqlalchemy import Column, Table, MetaData, Integer, String, ForeignKey, TIMESTAMP
import datetime
# from pathlib import Path
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.settings import settings

# BASE_DIR = Path(__file__).parent.parent

metadata = MetaData()

# users = Table(
#     "users",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("email", String, unique=True, nullable=False),
#     Column("password", String, nullable=False),
#     Column("registered_at", TIMESTAMP, default=datetime.datetime.utcnow),
# )
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)


async def async_main():
    engine = create_async_engine(settings.db_url, echo=settings.db_echo)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

        # await conn.execute(
        #     t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
        # )

    # async with engine.connect() as conn:
    # select a Result, which will be delivered with buffered
    # results
    # result = await conn.execute(select(t1).where(t1.c.name == "some name 1"))

    # print(result.fetchall())

    await engine.dispose()


asyncio.run(async_main())
