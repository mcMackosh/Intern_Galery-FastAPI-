from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps.role_check_dep import authorization
from app.models.membership import UserRole
from app.models.user import User
from app.services.image import image_service

router = APIRouter(prefix="/gallery/{gallery_id}/image", tags=["image"])


@router.post("/upload")
async def upload_images(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    files: list[UploadFile] = File(...),
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    return await image_service.upload_images(db, gallery_id, files)


@router.get("")
async def get_by_gallery(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.REGULAR, UserRole.ADMIN, UserRole.OWNER))],
    page: int = 1,
    limit: int = 20,
    order: str = "desc",
):
    return await image_service.get_images_by_gallery(db, gallery_id, page, limit, order)


@router.delete("")
async def delete_images(
    gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    ids: list[str],
):
    if not ids:
        raise HTTPException(status_code=400, detail="ids array is required")
    return await image_service.delete_images(db, ids, gallery_id)


@router.post("/move/{target_gallery_id}")
async def move_images(
    gallery_id: str,
    target_gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    ids: list[str],
):
    if not ids:
        raise HTTPException(status_code=400, detail="ids are required")
    return await image_service.move_images(db, ids, gallery_id, target_gallery_id)


@router.post("/copy/{target_gallery_id}")
async def copy_images(
    gallery_id: str,
    target_gallery_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(authorization(UserRole.ADMIN, UserRole.OWNER))],
    ids: list[str],
):
    if not ids:
        raise HTTPException(status_code=400, detail="ids are required")
    return await image_service.copy_images(db, ids, gallery_id, target_gallery_id)
