from typing import Annotated
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.helpers.security import decode_token
from app.models.user import User
from app.repositories.user_rep import user_repository

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        user_id: str | None = payload.get('sub')
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    user = await user_repository.get_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user