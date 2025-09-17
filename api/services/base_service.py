from sqlalchemy.ext.asyncio import AsyncSession


class BaseDBService:

    def __init__(self, session: AsyncSession):
        self._session = session
