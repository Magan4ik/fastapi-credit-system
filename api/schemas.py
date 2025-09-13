import datetime

from pydantic import BaseModel, Field, AfterValidator
from typing import Annotated, Optional
from . import validators

from db.models import User, Credit, Plan, Payment, Term


class UserDTO(BaseModel):
    login: Annotated[str, Field(max_length=255)]
    registration_date: datetime.date

    def to_orm(self):
        return User(**self.model_dump())


class CreditDTO(BaseModel):
    user_id: int
    issuance_date: datetime.date
    return_date: datetime.date
    actual_return_date: Optional[datetime.date]
    body: float
    percent: float

    def to_orm(self):
        return Credit(**self.model_dump())


class TermDTO(BaseModel):
    name: Annotated[str, Field(max_length=255)]

    def to_orm(self):
        return Term(**self.model_dump())


class PaymentDTO(BaseModel):
    sum: float
    payment_date: datetime.date
    credit_id: int
    type_id: int

    def to_orm(self):
        return Payment(**self.model_dump())


class PlanDTO(BaseModel):
    period: Annotated[datetime.date, AfterValidator(validators.first_day_date_validate)]
    sum: float
    category_id: int

    def to_orm(self):
        return Plan(**self.model_dump())


if __name__ == "__main__":
    user = UserDTO(login="TestLogin", registration_date=datetime.date(year=2025, month=9, day=1))
    print(user.registration_date)
