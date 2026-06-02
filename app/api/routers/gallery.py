from typing_extensions import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps.auth_dep import get_current_user
from app.core.deps.role_check_dep import authorization
from app.models.membership import UserRole
from app.models.user import User
from app.schemas.gallery_schema import CreateGalleryDto, GetGalleriesQueryDto, UpdateGalleryDto
from app.services.gallery import gallery_service

router = APIRouter(prefix="/gallery", tags=["gallery"])

@router.get("/{gallery_id}")
async def get_gallery(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.REGULAR, UserRole.ADMIN, UserRole.OWNER))],
):
    return await gallery_service.get_gallery_by_id(db, gallery_id)

@router.post("/")
async def create_gallery(
    dto: CreateGalleryDto,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await gallery_service.create_gallery(db, dto, current_user.id)

@router.get("/")
async def get_all_galleries(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(authorization())],
    options: Annotated[GetGalleriesQueryDto, Depends()],
    page: int = 1,
    limit: int = 3,
):
    return await gallery_service.get_all_galleries(db, current_user.id, page, limit, options)

@router.put("/{gallery_id}")
async def update_gallery(
    gallery_id: str,
    dto: UpdateGalleryDto,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
):
    return await gallery_service.update_gallery(db, gallery_id, dto)

@router.delete("/{gallery_id}")
async def delete_gallery(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.OWNER))],
):
    await gallery_service.delete_gallery(db, gallery_id)