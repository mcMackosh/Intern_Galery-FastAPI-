from fastapi import HTTPException, Response
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.helpers.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from app.core.redis import redis_service
from app.repositories.user_rep import user_repository
from app.schemas.user_schema import LoginDto, RegisterDto


class AuthService:
    async def register(self, db: AsyncSession, user_data: RegisterDto):
        existing_user = await user_repository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = await user_repository.create(db, user_data)
        
        access_token = create_access_token({'sub': user.id})
        refresh_token = create_refresh_token({'sub': user.id})
        
        await redis_service.set_refresh_token(user.id, refresh_token)
        return {"user": user, "access_token": access_token, "refresh_token": refresh_token}

    async def login(self, db: AsyncSession, dto: LoginDto):
        user = await user_repository.get_by_email(db, dto.email)
        if not user or not verify_password(dto.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token({'sub': user.id})
        refresh_token = create_refresh_token({'sub': user.id})
        
        await redis_service.set_refresh_token(user.id, refresh_token)
        return {"user": user, "access_token": access_token, "refresh_token": refresh_token}
    
    async def refresh_tokens(self, refresh_token: str):
        try:
            payload = decode_refresh_token(refresh_token)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id: str | None = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        saved_token = await redis_service.get_refresh_token(user_id)
        
        if not saved_token or saved_token != refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token({"sub": user_id})

        await redis_service.set_refresh_token(user_id, new_refresh_token)

        return {"access_token": access_token, "refresh_token": new_refresh_token}
        
    async def logout(self, user_id: str):
        deleted = await redis_service.remove_refresh_token(user_id)
        if not deleted:
            raise HTTPException(status_code=401, detail="Invalid session")
        return {"success": True}
        


auth_service = AuthService()
