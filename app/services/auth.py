from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.helpers.security import create_access_token, verify_password
from app.repositories.user import user_repository
from app.schemas.user_schema import LoginDto, RegisterDto


class AuthService:
    async def register(self, db: AsyncSession, user_data: RegisterDto):
        existing_user = await user_repository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return await user_repository.create(db, user_data)

    async def login(self, db: AsyncSession, dto: LoginDto):
        user = await user_repository.get_by_email(db, dto.email)
        if not user or not verify_password(dto.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token({"sub": user.id})
        return {"access_token": access_token}


auth_service = AuthService()
