import datetime


def date_month_range(first_day: datetime.date, last_day: datetime.date) -> list[tuple[datetime.date, datetime.date]]:
    dates = []
    current = first_day
    while current.month < last_day.month:
        next_month = current.replace(month=current.month + 1)
        dates.append((current, next_month - datetime.timedelta(days=1)))
        current = next_month
    dates.append((current, last_day))
    return dates
