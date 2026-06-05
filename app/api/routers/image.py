from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps.role_check_dep import authorization
from app.models.membership import UserRole
from app.models.user import User
from app.schemas.image_schema import (
    DeletedImagesResponse,
    IdsDto,
    ImageListResponse,
    ImageResponse,
)
from app.services.image_serv import image_service

router = APIRouter(prefix="/galleries/{gallery_id}/image", tags=["image"])


@router.post("/upload", response_model=list[ImageResponse])
async def upload_images(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    images: list[UploadFile] = File(...),
):
    if not images:
        raise HTTPException(status_code=400, detail="No files provided")
    return await image_service.upload_images(db, gallery_id, images)


@router.get("", response_model=ImageListResponse)
async def get_by_gallery(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.REGULAR, UserRole.ADMIN, UserRole.OWNER))],
    page: int = 1,
    limit: int = 20,
    order: str = "desc",
):
    return await image_service.get_images_by_gallery(db, gallery_id, page, limit, order)


@router.delete("", response_model=DeletedImagesResponse)
async def delete_images(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    body: IdsDto,
):
    if not body.ids:
        raise HTTPException(status_code=400, detail="ids array is required")
    return await image_service.delete_images(db, body.ids, gallery_id)


@router.post("/move/{target_gallery_id}", response_model=list[ImageResponse])
async def move_images(
    gallery_id: str,
    target_gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    body: IdsDto,
):
    if not body.ids:
        raise HTTPException(status_code=400, detail="ids are required")
    return await image_service.move_images(db, body.ids, gallery_id, target_gallery_id)


@router.post("/copy/{target_gallery_id}", response_model=list[ImageResponse])
async def copy_images(
    gallery_id: str,
    target_gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    body: IdsDto,
):
    if not body.ids:
        raise HTTPException(status_code=400, detail="ids are required")
    return await image_service.copy_images(db, body.ids, gallery_id, target_gallery_id)
