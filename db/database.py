from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    engine = create_async_engine(settings.database_url, echo=settings.debug)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def save(self):
        async with self.async_session() as session:
            session.add(self)
            await session.commit()
