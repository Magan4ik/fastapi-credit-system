import datetime

from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, func, Numeric, String


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(255))
    registration_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())

    credits: Mapped[list["Credit"]] = relationship(back_populates='user', cascade="all, delete-orphan", lazy="joined")


class Credit(Base):
    __tablename__ = "credits"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    issuance_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())
    return_date: Mapped[datetime.date] = mapped_column(Date)
    actual_return_date: Mapped[datetime.date] = mapped_column(Date)
    body: Mapped[int]
    percent: Mapped[float] = mapped_column(Numeric(3, 2))

    user: Mapped[User] = relationship(back_populates="credits", lazy="joined")
    payments: Mapped[list["Payment"]] = relationship(back_populates="payment", cascade="all, delete-orphan", lazy="joined")


class Term(Base):
    __tablename__ = "dictionary"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sum: Mapped[int]
    payment_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())
    credit_id: Mapped[Credit] = mapped_column(ForeignKey("credits.id"))
    type_id: Mapped[Term] = mapped_column(ForeignKey("dictionary.id"))

    credit: Mapped[Credit] = relationship(back_populates="payments", lazy="joined")
    type: Mapped[Term] = relationship(lazy="joined")


class Plan(Base):
    __tablename__ = "plans"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period: Mapped[datetime.date] = mapped_column(Date)
    sum: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"))

    category: Mapped[Term] = relationship(lazy="joined")
