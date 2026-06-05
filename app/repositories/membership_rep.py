from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.membership import Membership, UserRole


class MembershipRepository:
    async def get_members(self, db: AsyncSession, gallery_id: str) -> list[Membership]:
        result = await db.execute(
            select(Membership)
            .where(Membership.gallery_id == gallery_id)
            .options(selectinload(Membership.user))
        )
        return list(result.scalars().all())

    async def get_member(
        self, db: AsyncSession, gallery_id: str, user_id: str
    ) -> Membership | None:
        result = await db.execute(
            select(Membership).where(
                and_(Membership.gallery_id == gallery_id, Membership.user_id == user_id)
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self, db: AsyncSession, gallery_id: str, user_id: str, role: UserRole
    ) -> Membership:
        membership = Membership(user_id=user_id, gallery_id=gallery_id, role=role)
        db.add(membership)
        await db.commit()
        await db.refresh(membership)
        return membership

    async def update(
        self, db: AsyncSession, membership: Membership, role: UserRole
    ) -> Membership:
        membership.role = role
        await db.commit()
        await db.refresh(membership)
        return membership

    async def delete(self, db: AsyncSession, membership: Membership) -> None:
        await db.delete(membership)
        await db.commit()


membership_repository = MembershipRepository()
