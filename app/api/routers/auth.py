from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.models.user import User
from app.schemas.user_schema import AccessTokenResponse, LoginDto, RegisterDto
from app.services.auth_serv import auth_service

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/register", response_model=AccessTokenResponse)
async def register(
    user_data: RegisterDto,
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
):
    data = await auth_service.register(db, user_data)
    response.set_cookie(key="refresh_token", value=data['refresh_token'], httponly=True, samesite="lax", max_age=60 * 60 * 48)
    return AccessTokenResponse(access_token=data['access_token'])


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    dto: LoginDto,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    data = await auth_service.login(db, dto)
    response.set_cookie(key="refresh_token", value=data['refresh_token'], httponly=True, samesite="lax", max_age=60 * 60 * 48)
    return AccessTokenResponse(access_token=data['access_token'])


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    data = await auth_service.refresh_tokens(refresh_token)
    response.set_cookie(key="refresh_token", value=data['refresh_token'], httponly=True, samesite="lax", max_age=60 * 60 * 48)
    return AccessTokenResponse(access_token=data['access_token'])


@router.post("/logout")
async def logout(
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    await auth_service.logout(current_user.id)
    response.delete_cookie("refresh_token")
    return {}
