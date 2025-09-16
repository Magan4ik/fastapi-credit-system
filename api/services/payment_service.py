import datetime
from typing import Optional
from abc import ABC, abstractmethod

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Payment


# noinspection PyTypeChecker
class PaymentService:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_payments_in_range(self, start_date: datetime.date, end_date: datetime.date) -> list[Payment]:
        stmt = select(Payment).where(and_(
            start_date <= Payment.payment_date,
            end_date >= Payment.payment_date
        ))
        payments = (await self._session.scalars(stmt)).unique().all()
        return payments

    @staticmethod
    def calculate_performance_info(payments: list[Payment],
                                   start_date: Optional[datetime.date] = None,
                                   end_date: Optional[datetime.date] = None) -> tuple[float, int]:
        if start_date and end_date:
            payments = list(filter(lambda pm: start_date <= pm.payment_date <= end_date, payments))
        payment_sum = sum(pm.sum for pm in payments)
        amount_payments = len(payments)
        return payment_sum, amount_payments
