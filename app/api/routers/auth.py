from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.models.user import User
from app.services.auth import auth_service
from app.schemas.user_schema import LoginDto, RegisterDto, UserResponce
from fastapi import HTTPException

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/register")
async def register(user_data: RegisterDto, db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    data = await auth_service.register(db, user_data)
    response.set_cookie(key="refresh_token", value=data['refresh_token'], httponly=True)
    return {"access_token": data['access_token'], "user": UserResponce.model_validate(data['user'])}

@router.post("/login")
async def login(dto: LoginDto, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    data = await auth_service.login(db, dto)
    response.set_cookie(key="refresh_token", value=data['refresh_token'], httponly=True)
    return {"access_token": data['access_token'], "user": UserResponce.model_validate(data['user'])}

@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    data = await auth_service.refresh_tokens(refresh_token)
    response.set_cookie(key="refresh_token", value=data['refresh_token'], httponly=True)
    return {"access_token": data['access_token'], "user": UserResponce.model_validate(data['user'])}

@router.post("/logout")
async def logout(response: Response, current_user: Annotated[User, Depends(get_current_user)]):
    await auth_service.logout(current_user.id)
    response.delete_cookie("refresh_token")
    return {"success": True}