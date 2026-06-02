from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.membership import UserRole
from app.repositories.gallery import gallery_repository
from app.repositories.membership import membership_repository
from app.schemas.gallery_schema import CreateGalleryDto, GetGalleriesQueryDto, UpdateGalleryDto


class GalleryService:

    async def get_gallery_by_id(self, db: AsyncSession, gallery_id: str):
        gallery = await gallery_repository.get_by_id(db, gallery_id)
        if not gallery:
            raise HTTPException(status_code=404, detail="Gallery not found")
        return gallery

    async def create_gallery(self, db: AsyncSession, dto: CreateGalleryDto, user_id: str):
        gallery = await gallery_repository.create(db, dto)
        await membership_repository.create(db, gallery.id, user_id, UserRole.OWNER)
        return gallery

    async def get_all_galleries(
        self,
        db: AsyncSession,
        user_id: str,
        page: int,
        limit: int,
        options: GetGalleriesQueryDto,
    ):
        return await gallery_repository.get_all_for_user(db, user_id, page, limit, options)

    async def update_gallery(self, db: AsyncSession, gallery_id: str, dto: UpdateGalleryDto):
        gallery = await gallery_repository.get_by_id(db, gallery_id)
        if not gallery:
            raise HTTPException(status_code=404, detail="Gallery not found")
        return await gallery_repository.update(db, gallery, dto)

    async def delete_gallery(self, db: AsyncSession, gallery_id: str):
        gallery = await gallery_repository.get_by_id(db, gallery_id)
        if not gallery:
            raise HTTPException(status_code=404, detail="Gallery not found")
        await gallery_repository.delete(db, gallery)
        
        
gallery_service = GalleryService()