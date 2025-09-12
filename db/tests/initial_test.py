import datetime

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..models import User, Credit, Term, Payment, Plan

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(DATABASE_URL_TEST, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_session(async_engine):
    async_session_maker = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session_maker() as session:
        yield session


@pytest.mark.anyio
async def test_create_user(async_session):
    user = User(login="TestLogin")
    async_session.add(user)
    await async_session.commit()

    await async_session.refresh(user)

    u = await async_session.get(User, user.id)
    assert u is not None
    assert u.login == "TestLogin"


@pytest.mark.anyio
async def test_create_credit(async_session):
    credit = Credit(user_id=1,
                    return_date=datetime.date.fromisoformat("2025-09-30"),
                    actual_return_date=datetime.date.fromisoformat("2025-10-09"),
                    body=1000,
                    percent=0.5)
    async_session.add(credit)
    await async_session.commit()

    await async_session.refresh(credit)

    c = await async_session.get(Credit, credit.id)
    assert c is not None
    assert c.user.login == "TestLogin"
    assert c.return_date < c.actual_return_date


@pytest.mark.anyio
async def test_create_term(async_session):
    term = Term(name="TestName")
    async_session.add(term)
    await async_session.commit()

    await async_session.refresh(term)

    t = await async_session.get(Term, term.id)
    assert t is not None
    assert t.name == "TestName"


@pytest.mark.anyio
async def test_create_payment(async_session):
    payment = Payment(sum=1000, credit_id=1, type_id=1)
    async_session.add(payment)
    await async_session.commit()

    await async_session.refresh(payment)

    p = await async_session.get(Payment, payment.id)
    assert p is not None
    assert p.credit.user.login == "TestLogin"
    assert p.type.name == "TestName"


@pytest.mark.anyio
async def test_create_plan(async_session):
    plan = Plan(period=datetime.date.fromisoformat("2025-09-30"), sum=1000, category_id=1)
    async_session.add(plan)
    await async_session.commit()

    await async_session.refresh(plan)

    p = await async_session.get(Plan, plan.id)
    assert p is not None
    assert str(p.period) == "2025-09-30"
    assert p.category.name == "TestName"
