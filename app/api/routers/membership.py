from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.core.deps.role_check_dep import authorization
from app.models.membership import UserRole
from app.models.user import User
from app.schemas.membership_schema import (
    CreateOrUpdateMembershipDto,
    MemberResponse,
    MembershipUpsertResponse,
)
from app.services.membership_serv import membership_service

router = APIRouter(prefix="/gallery/{gallery_id}/members", tags=["membership"])


@router.get("/", response_model=list[MemberResponse])
async def get_members(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.REGULAR, UserRole.ADMIN, UserRole.OWNER))],
):
    return await membership_service.get_members(db, gallery_id)


@router.post("/create-or-update", response_model=MembershipUpsertResponse)
async def create_or_update(
    gallery_id: str,
    body: CreateOrUpdateMembershipDto,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await membership_service.create_or_update(
        db, gallery_id, body.user_id, body.role, current_user
    )


@router.delete("/{user_id}")
async def delete_member(
    gallery_id: str,
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await membership_service.delete_member(db, gallery_id, user_id, current_user)
    return True


@router.delete("/")
async def leave_gallery(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await membership_service.leave_gallery(db, gallery_id, current_user)
    return True
