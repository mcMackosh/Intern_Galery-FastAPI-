from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.auth import auth_service
from app.schemas.user_schema import LoginDto, RegisterDto

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/register")
async def register(user_data: RegisterDto, db: Annotated[AsyncSession, Depends(get_db)]):
    return await auth_service.register(db, user_data)


@router.post("/login")
async def login(dto: LoginDto, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    login_data = await auth_service.login(db, dto)
    response.set_cookie(key="refresh_token", value=login_data['access_token'], httponly=True)
    return login_data