import datetime


def first_day_date_validate(date: datetime.date) -> datetime.date:
    if date.day == 1:
        return date
    raise ValueError("The date should be the first day of the month")