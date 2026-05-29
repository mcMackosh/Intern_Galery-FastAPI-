from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.helpers.security import hash_password
from app.models.user import User
from app.schemas.user_schema import RegisterDto


class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user_data: RegisterDto) -> User:
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        print(user)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


user_repository = UserRepository()
