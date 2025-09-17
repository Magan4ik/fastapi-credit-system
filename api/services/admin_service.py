from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.auth import AdminDTO
from api.services.base_service import BaseDBService
from core.utils import get_password_hash
from db.models import Admin


class AdminService(BaseDBService):

    async def get_admin(self, username: str) -> Admin:
        stmt = select(Admin).where(Admin.username == username)
        admin = await self._session.scalar(stmt)
        return admin

    async def create_admin(self, admin_dto: AdminDTO) -> Admin:
        hashed_password = get_password_hash(admin_dto.password)
        admin = Admin(username=admin_dto.username, password=hashed_password)
        self._session.add(admin)
        await self._session.commit()
        return admin
