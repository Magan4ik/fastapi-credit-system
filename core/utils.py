import datetime
from typing import Optional

import jwt
from passlib.context import CryptContext

from core.config import settings
from db.models import Admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def date_month_range(first_day: datetime.date, last_day: datetime.date) -> list[tuple[datetime.date, datetime.date]]:
    dates = []
    current = first_day
    while current.month < last_day.month:
        next_month = current.replace(month=current.month + 1)
        dates.append((current, next_month - datetime.timedelta(days=1)))
        current = next_month
    dates.append((current, last_day))
    return dates


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(admin_service: "AdminService", username: str, password: str) -> Optional[Admin]:
    user = await admin_service.get_admin(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
