from core.settings import settings
import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    async_sessionmaker,
    AsyncSession
)
from .models import metadata


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.metadata = metadata
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=asyncio.current_task,
        )
        # return session
        try:
            async with session() as s:
                yield s
        finally:
            await session.remove()

    # async def scoped_session_dependency(self) -> AsyncSession:
    #     session = self.get_scoped_session()
    #     print(type(session))
    #     yield session
    #     await session.close()



db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
