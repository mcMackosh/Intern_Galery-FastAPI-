from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.models.user import User
from app.schemas.user_schema import ChangePasswordDto, UpdateProfileDto, UserResponse
from app.services.profile_serv import profile_service

router = APIRouter(prefix='/profile', tags=['profile'])


@router.get("/", response_model=UserResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@router.patch("/", response_model=UserResponse)
async def update_profile(
    dto: UpdateProfileDto,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    return await profile_service.update_profile(db, current_user, dto)


@router.patch("/change-password", response_model=UserResponse)
async def change_password(
    dto: ChangePasswordDto,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    return await profile_service.change_password(db, current_user, dto)
