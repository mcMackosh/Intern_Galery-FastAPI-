from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.models.membership import UserRole
from app.models.user import User
from app.repositories.membership import membership_repository


def authorization(*roles: UserRole):
    if not roles:
        async def auth_only(
            current_user: Annotated[User, Depends(get_current_user)],
        ) -> User:
            return current_user
        return auth_only

    async def auth_with_roles(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        gallery_id: str,
        target_gallery_id: str | None = None,
    ) -> User:
        gallery_ids = [gid for gid in [gallery_id, target_gallery_id] if gid]
        
        for gid in gallery_ids:
            membership = await membership_repository.get_member(db, gid, current_user.id)

            if not membership:
                raise HTTPException(status_code=403, detail=f"You have no permissions for gallery {gid}")

            if membership.role == UserRole.OWNER:
                continue

            if membership.role not in roles:
                raise HTTPException(status_code=403, detail=f"Not enough permissions for gallery {gid}")

        return current_user

    return auth_with_roles