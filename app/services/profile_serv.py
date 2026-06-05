from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.helpers.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_rep import user_repository
from app.schemas.user_schema import ChangePasswordDto, UpdateProfileDto


class ProfileService:
    async def update_profile(
        self, db: AsyncSession, user: User, dto: UpdateProfileDto
    ) -> User:
        if dto.email is not None:
            existing = await user_repository.get_by_email(db, dto.email)
            if existing and existing.id != user.id:
                raise HTTPException(status_code=409, detail="Email already in use")
        return await user_repository.update(db, user, dto)

    async def change_password(
        self, db: AsyncSession, user: User, dto: ChangePasswordDto
    ) -> User:
        if not verify_password(dto.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Old password is incorrect")
        return await user_repository.update_password(
            db, user, hash_password(dto.new_password)
        )


profile_service = ProfileService()
