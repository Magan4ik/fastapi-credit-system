from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.auth import Token, AdminDTO
from api.services.admin_service import AdminService
from core.config import settings
from core.utils import authenticate_user, create_access_token
from db.database import get_session

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
) -> Token:
    admin_service = AdminService(db)
    user = await authenticate_user(admin_service, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/create_admin")
async def create_admin(admin: AdminDTO, db: AsyncSession = Depends(get_session)):
    admin_service = AdminService(db)
    try:
        await admin_service.create_admin(admin)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already taken")
    return JSONResponse(None, status_code=201)

