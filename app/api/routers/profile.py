from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends
from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.models.membership import UserRole
from app.models.user import User
from app.schemas.user_schema import UserResponce
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/profile', tags=['profile'])

@router.post("/", response_model=UserResponce)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user