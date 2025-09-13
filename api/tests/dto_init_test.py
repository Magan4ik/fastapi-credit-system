import datetime

from ..schemas import UserDTO, CreditDTO


def test_user():
    user = UserDTO(login="TestLogin", registration_date=datetime.date(year=2025, month=9, day=1))


def test_credit():
    credit = CreditDTO(user_id=1,
                       issuance_date=datetime.date(year=2025, month=11, day=1),
                       return_date=datetime.date(year=2026, month=4, day=1),
                       actual_return_date=None,
                       body=1000,
                       percent=0.02
                       )

