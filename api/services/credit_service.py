import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from api.services.base_service import BaseDBService
from db.models import Credit, Payment
from api.schemas.responses import ClosedUserCreditResponse, OpenedUserCreditResponse
from api.schemas.models_dto import CreditDTO


# noinspection PyTypeChecker
class CreditService(BaseDBService):

    async def collect_credit_info(self, user_id: int) -> list[ClosedUserCreditResponse | OpenedUserCreditResponse]:
        credits = await self.get_user_credit(user_id)
        response = []
        for credit in credits:
            closed = credit.actual_return_date is not None
            credit_dto = CreditDTO.from_orm(credit)
            if not closed:
                # TODO: Рассмотреть более удачный вариант получения текущего времени
                debt = (datetime.datetime.now().date() - credit.return_date).days
                body_payments = list(filter(lambda p: p.type.name == "тіло", credit.payments))
                percent_payments = list(filter(lambda p: p.type.name == "відсотки", credit.payments))
                response.append(OpenedUserCreditResponse(
                    **credit_dto.dict(exclude={"user_id", "actual_return_date"}),
                    debt=debt,
                    body_payments=sum(pm.sum for pm in body_payments),
                    percent_payments=sum(pm.sum for pm in percent_payments),
                    closed=closed
                ))
            else:
                response.append(ClosedUserCreditResponse(
                    **credit_dto.dict(exclude={"user_id", "return_date"}),
                    closed=closed,
                    all_payments=sum(pm.sum for pm in credit.payments),
                ))

        return response

    async def get_user_credit(self, user_id: int) -> list[Credit]:
        stmt = select(Credit).where(Credit.user_id == user_id)
        credits = (await self._session.scalars(stmt)).unique().all()
        return credits

    async def get_credits_in_range(self, start_date: datetime.date, end_date: datetime.date) -> list[Credit]:
        stmt = select(Credit).where(and_(
            start_date <= Credit.issuance_date,
            end_date >= Credit.issuance_date
        ))
        credits = (await self._session.scalars(stmt)).unique().all()
        return credits

    @staticmethod
    def calculate_performance_info(credits: list[Credit],
                                   start_date: Optional[datetime.date] = None,
                                   end_date: Optional[datetime.date] = None) -> tuple[float, int]:
        if start_date and end_date:
            credits = list(filter(lambda cr: start_date <= cr.issuance_date <= end_date, credits))
        credit_sum = sum(cr.body for cr in credits)
        amount_credits = len(credits)
        return credit_sum, amount_credits
