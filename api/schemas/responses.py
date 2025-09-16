import datetime
from typing import Optional

from pydantic import BaseModel


class BaseUserCreditResponse(BaseModel):
    issuance_date: datetime.date
    closed: bool
    body: float
    percent: float


class ClosedUserCreditResponse(BaseUserCreditResponse):
    actual_return_date: Optional[datetime.date]
    all_payments: float


class OpenedUserCreditResponse(BaseUserCreditResponse):
    return_date: datetime.date
    debt: int
    body_payments: float
    percent_payments: float


class PlanPerformanceResponse(BaseModel):
    month: datetime.date
    category: str
    sum: float
    real_sum: float
    percent: float


class MonthPerformanceResponse(BaseModel):
    month_year: str
    credit_amount: int
    plan_credit_sum: float
    credit_sum: float
    credit_percent: float

    payment_amount: int
    plan_payment_sum: float
    payment_sum: float
    payment_percent: float

    annual_credit_percent: float
    annual_payment_percent: float
