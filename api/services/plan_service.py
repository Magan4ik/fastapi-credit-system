import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.models_dto import PlanDTO
from api.schemas.responses import PlanPerformanceResponse, MonthPerformanceResponse
from db.models import Plan


class PlanService:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_plan_performance(self, date: datetime.date, credits_sum: float, payments_sum: float) -> list[PlanPerformanceResponse]:
        plans = await self.get_plan_by_month(date)
        response = []
        for plan in plans:
            real_sum = credits_sum if plan.category.name == "видача" else payments_sum
            response.append(PlanPerformanceResponse(
                month=date,
                category=plan.category.name,
                sum=plan.sum,
                real_sum=real_sum,
                percent=round(real_sum / plan.sum, 2) * 100
            ))

        return response

    async def get_month_performance(self,
                                    date: datetime.date,
                                    annual_credit_sum: float, annual_payment_sum: float,
                                    month_credit_sum: float, month_payment_sum: float,
                                    amount_credit: int, amount_payment: int) -> MonthPerformanceResponse:
        plans = await self.get_plan_by_month(date)
        if len(plans) != 2:
            raise ValueError("not enough plans")

        credit_plan, payment_plan = sorted(plans, key=lambda p: p.category.name == "збір")
        performance = MonthPerformanceResponse(
            month_year=date.strftime("%B %Y"),
            credit_amount=amount_credit,
            plan_credit_sum=credit_plan.sum,
            credit_sum=month_credit_sum,
            credit_percent=round(month_credit_sum / credit_plan.sum, 2) * 100,
            payment_amount=amount_payment,
            plan_payment_sum=payment_plan.sum,
            payment_sum=month_payment_sum,
            payment_percent=round(month_payment_sum / payment_plan.sum, 2) * 100,
            annual_credit_percent=round(month_credit_sum / annual_credit_sum, 2) * 100,
            annual_payment_percent=round(month_payment_sum / annual_payment_sum, 2) * 100
        )

        return performance

    # noinspection PyTypeChecker
    async def get_plan_by_month(self, date: datetime.date) -> list[Plan]:
        stmt = select(Plan).where(Plan.period == date)
        plans = (await self._session.scalars(stmt)).unique().all()
        return plans

    # noinspection PyTypeChecker
    async def get_plan_by_month_n_category(self, date: datetime.date, category_id: int) -> list[Plan]:
        stmt = select(Plan).where(and_(Plan.period == date, Plan.category_id == category_id))
        plans = (await self._session.scalars(stmt)).unique().all()
        return plans

    async def insert_plans(self, plans: list[PlanDTO]):
        for plan in plans:
            plan_model = plan.to_orm()
            self._session.add(plan_model)
        await self._session.commit()
