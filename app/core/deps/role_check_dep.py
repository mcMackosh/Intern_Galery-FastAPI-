from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.deps.auth_deps import get_current_user
from app.models.membership import UserRole
from app.models.user import User
from app.repositories.membership import membership_repository

def require_gallery_roles(*roles: UserRole):
    async def require_gallery_roles_guard(
        gallery_id: str,
        db:  Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> UserRole:
        membership = await membership_repository.get_member(db, gallery_id, current_user.id)
        
        if not membership:
            raise HTTPException(status_code=403, detail="You have no permissions for this gallery")
        
        if membership.role == UserRole.OWNER:
            return membership.role
        
        if membership.role not in roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        return membership.role
    
    return require_gallery_roles_guard