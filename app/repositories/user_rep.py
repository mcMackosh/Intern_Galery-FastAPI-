from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.helpers.security import hash_password
from app.models.user import User
from app.schemas.user_schema import RegisterDto, UpdateProfileDto


class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id: str) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user_data: RegisterDto) -> User:
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update(self, db: AsyncSession, user: User, dto: UpdateProfileDto) -> User:
        for field, value in dto.model_dump(exclude_none=True).items():
            setattr(user, field, value)
        await db.commit()
        await db.refresh(user)
        return user

    async def update_password(
        self, db: AsyncSession, user: User, new_hashed_password: str
    ) -> User:
        user.hashed_password = new_hashed_password
        await db.commit()
        await db.refresh(user)
        return user


user_repository = UserRepository()
