from db.parsers.importers import ModelImporter
from .conf import *
from ..models import User, Credit, Plan, Payment, Term


@pytest.mark.anyio
async def test_dataset_import(async_session):
    await ModelImporter.start(async_session)
    async with async_session.begin():
        user = await async_session.get(User, 31)
        credit = await async_session.get(Credit, 31)
        plan = await async_session.get(Plan, 31)
        payment = await async_session.get(Payment, 31)
        term = await async_session.get(Term, 3)

    assert user.login == "pageantrylamentable"
    assert credit.body == 2000
    assert plan.sum == 166000
    assert float(payment.sum) == 555.56
    assert term.name == "видача"

