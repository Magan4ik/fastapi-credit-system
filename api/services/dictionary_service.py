from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.base_service import BaseDBService
from db.models import Term


class DictionaryService(BaseDBService):

    async def get_all_terms(self):
        stmt = select(Term)
        terms = (await self._session.scalars(stmt)).unique().all()
        return terms

    async def get_term_by_name(self, name: str) -> Term:
        stmt = select(Term).where(Term.name == name)
        term = await self._session.scalar(stmt)
        return term
