from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.membership import UserRole
from app.models.user import User
from app.repositories.membership import membership_repository

class MembershipService:

    async def _get_caller_role(
        self, db: AsyncSession, gallery_id: str, current_user: User
    ) -> UserRole:
        current_membership = await membership_repository.get_member(db, gallery_id, current_user.id)
        if not current_membership:
            raise HTTPException(status_code=403, detail="You are not a member of this gallery")
        return current_membership.role

    async def get_members(self, db: AsyncSession, gallery_id: str):
        return await membership_repository.get_members(db, gallery_id)

    async def create_or_update(
        self,
        db: AsyncSession,
        gallery_id: str,
        user_id: str,
        role: UserRole,
        current_user: User,
    ):
        caller_role = await self._get_caller_role(db, gallery_id, current_user)
        existing = await membership_repository.get_member(db, gallery_id, user_id)

        if caller_role == UserRole.OWNER and current_user.id == user_id and role != UserRole.OWNER:
            raise HTTPException(status_code=400, detail='Owner cannot demote themselves')

        if caller_role == UserRole.ADMIN and role != UserRole.REGULAR:
            raise HTTPException(status_code=400, detail='Admin can assign only REGULAR role')

        if existing:
            if caller_role == UserRole.ADMIN and existing.role != UserRole.REGULAR:
                raise HTTPException(status_code=400, detail='Admin can manage only REGULAR members')

            if existing.role == UserRole.OWNER and caller_role != UserRole.OWNER:
                raise HTTPException(status_code=400, detail='Only OWNER can modify OWNER membership')

            return await membership_repository.update(db, existing, role)

        return await membership_repository.create(db, gallery_id, user_id, role)

    async def delete_member(
        self,
        db: AsyncSession,
        gallery_id: str,
        user_id: str,
        current_user: User,
    ):
        caller_role = await self._get_caller_role(db, gallery_id, current_user)
        membership = await membership_repository.get_member(db, gallery_id, user_id)

        if not membership:
            raise HTTPException(status_code=404, detail="Member not found")

        if caller_role == UserRole.ADMIN and membership.role != UserRole.REGULAR:
            raise HTTPException(status_code=400, detail='Admin can delete only REGULAR members')

        if membership.role == UserRole.OWNER and caller_role != UserRole.OWNER:
            raise HTTPException(status_code=400, detail='Only OWNER can delete OWNER')

        await membership_repository.delete(db, membership)

    async def leave_gallery(
        self,
        db: AsyncSession,
        gallery_id: str,
        current_user: User,
    ):
        membership = await membership_repository.get_member(db, gallery_id, current_user.id)

        if not membership:
            raise HTTPException(status_code=404, detail="You are not a member of this gallery")

        await membership_repository.delete(db, membership)


membership_service = MembershipService()