import datetime
from typing import Optional

from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, func, Numeric, String


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(255))
    registration_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.current_date())

    credits: Mapped[list["Credit"]] = relationship(back_populates='user', cascade="all, delete-orphan", lazy="joined")


class Credit(Base):
    __tablename__ = "credits"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    issuance_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.current_date())
    return_date: Mapped[datetime.date] = mapped_column(Date)
    actual_return_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True, default=None)
    body: Mapped[float] = mapped_column(Numeric(10, 2))
    percent: Mapped[float] = mapped_column(Numeric(10, 2))

    user: Mapped[User] = relationship(back_populates="credits", lazy="joined")
    payments: Mapped[list["Payment"]] = relationship(back_populates="credit", cascade="all, delete-orphan", lazy="joined")


class Term(Base):
    __tablename__ = "dictionary"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sum: Mapped[float] = mapped_column(Numeric(10, 2))
    payment_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.current_date())
    credit_id: Mapped[int] = mapped_column(ForeignKey("credits.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"))

    credit: Mapped[Credit] = relationship(back_populates="payments", lazy="joined")
    type: Mapped[Term] = relationship(lazy="joined")


class Plan(Base):
    __tablename__ = "plans"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period: Mapped[datetime.date] = mapped_column(Date)
    sum: Mapped[float] = mapped_column(Numeric(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"))

    category: Mapped[Term] = relationship(lazy="joined")


# В структурі таблиці Users в ТЗ не вказано поле пароля. Так само його немає в тестових даних.
# Але JWT авторизацію без пароля робити небезпечно. Я висунув припущення, що users це клієнти, а не безпосередньо користувачі.
# Тому ця модель (Admin) має відображати адміністратора, який має доступ до операцій з кредитами, платежами та планами.
class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
