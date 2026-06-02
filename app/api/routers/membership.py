from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.models.membership import UserRole
from app.models.user import User
from app.schemas.membership_schema import CreateOrUpdateMembershipDto, MembershipResponse
from app.services.membership import membership_service

router = APIRouter(prefix="/gallery/{gallery_id}/members", tags=["membership"])


@router.get("/", response_model=list[MembershipResponse])
async def get_members(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await membership_service.get_members(db, gallery_id)


@router.post("/create-or-update", response_model=MembershipResponse)
async def create_or_update(
    gallery_id: str,
    body: CreateOrUpdateMembershipDto,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
    
):
    return await membership_service.create_or_update(
        db, gallery_id, body.user_id, body.role, current_user
    )

@router.delete("/{user_id}", status_code=204)
async def delete_member(
    gallery_id: str,
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await membership_service.delete_member(db, gallery_id, user_id, current_user)

@router.delete("/", status_code=204)
async def leave_gallery(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await membership_service.leave_gallery(db, gallery_id, current_user)