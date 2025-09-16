import datetime

from fastapi import FastAPI, APIRouter, Depends, HTTPException, File
from pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.models_dto import PlanDTO
from api.schemas.responses import MonthPerformanceResponse, PlanPerformanceResponse, ClosedUserCreditResponse, \
    OpenedUserCreditResponse
from api.services.dictionary_service import DictionaryService
from api.services.payment_service import PaymentService
from core.utils import date_month_range
from db.database import get_session
from api.services.credit_service import CreditService
from api.services.plan_service import PlanService
from db.parsers.converters import TermNameConverter, Converter
from db.parsers.parsers import UniversalParser
from db.parsers.readers import ExcelReader

from typing import Annotated

app = FastAPI()
router = APIRouter()


@router.get("/user_credits/{user_id}")
async def user_credits(user_id: int, db: AsyncSession = Depends(get_session)) -> list[ClosedUserCreditResponse | OpenedUserCreditResponse]:
    credit_service = CreditService(db)
    response = await credit_service.collect_credit_info(user_id)
    if not response:
        raise HTTPException(status_code=404)
    return response


@router.get("/plans_performance")
async def plans_performance(date: datetime.date, db: AsyncSession = Depends(get_session)) -> list[PlanPerformanceResponse]:
    month = date.replace(day=1)

    plan_service = PlanService(db)
    credit_service = CreditService(db)
    payments_service = PaymentService(db)

    month_credits = await credit_service.get_credits_in_range(start_date=month, end_date=date)
    month_payments = await payments_service.get_payments_in_range(start_date=month, end_date=date)
    credits_sum = sum(cr.body for cr in month_credits)
    payments_sum = sum(pm.sum for pm in month_payments)

    response = await plan_service.get_plan_performance(month, credits_sum, payments_sum)
    if not response:
        raise HTTPException(status_code=404)
    return response


@router.get("/year_performance")
async def year_performance(year: int, db: AsyncSession = Depends(get_session)) -> list[MonthPerformanceResponse]:
    plan_service = PlanService(db)
    credit_service = CreditService(db)
    payments_service = PaymentService(db)

    try:
        first_day = datetime.date(year=year, month=1, day=1)
        now = datetime.datetime.now()
        last_day = now.date() if year == now.year else first_day.replace(month=12, day=31)
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect year")

    dates = date_month_range(first_day, last_day)

    credits = await credit_service.get_credits_in_range(first_day, last_day)
    payments = await payments_service.get_payments_in_range(first_day, last_day)
    annual_credit_sum = sum(cr.body for cr in credits)
    annual_payment_sum = sum(pm.sum for pm in payments)
    response = []
    for month_start, month_end in dates:
        month_credit_sum, amount_credits = CreditService.calculate_performance_info(credits, month_start, month_end)
        month_payment_sum, amount_payments = PaymentService.calculate_performance_info(payments, month_start, month_end)
        try:
            month_performance = await plan_service.get_month_performance(month_start,
                                                                         annual_credit_sum, annual_payment_sum,
                                                                         month_credit_sum, month_payment_sum,
                                                                         amount_credits, amount_payments)
        except ValueError:
            continue
        response.append(month_performance)

    return response


@router.post("/plans_insert")
async def plans_insert(file: Annotated[bytes, File()], db: AsyncSession = Depends(get_session)):
    dictionary_service = DictionaryService(db)
    dictionary_cache = await dictionary_service.get_all_terms()
    plan_service = PlanService(db)

    period_converter = Converter("Період", "period")
    sum_converter = Converter("Сума", "sum")
    term_converter = TermNameConverter("Назва категорії", "category_id", dictionary_cache)

    plan_parser = UniversalParser(ExcelReader(), PlanDTO, period_converter, sum_converter, term_converter)
    try:
        plans = plan_parser.parse(file)
    except ValidationError:
        raise HTTPException(status_code=400, detail="bad data in file")

    for plan in plans:
        plan_models = await plan_service.get_plan_by_month_n_category(plan.period, plan.category_id)
        if plan_models:
            raise HTTPException(status_code=400, detail=f"Plan ({plan.period} {plan.category_id}) already exists")

    await plan_service.insert_plans(plans)

    return "Плани внесені"


app.include_router(router)
