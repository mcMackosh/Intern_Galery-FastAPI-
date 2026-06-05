import math

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.membership import UserRole
from app.repositories.gallery_rep import gallery_repository
from app.repositories.membership_rep import membership_repository
from app.schemas.gallery_schema import CreateGalleryDto, GetGalleriesQueryDto, UpdateGalleryDto


class GalleryService:

    async def get_gallery_by_id(
        self, db: AsyncSession, gallery_id: str, user_id: str | None = None
    ):
        gallery = await gallery_repository.get_by_id(db, gallery_id)
        if not gallery:
            raise HTTPException(status_code=404, detail="Gallery not found")

        role = None
        if user_id:
            membership = await membership_repository.get_member(db, gallery_id, user_id)
            role = membership.role if membership else None

        return {
            'id': gallery.id,
            'title': gallery.title,
            'created_at': gallery.created_at,
            'role': role,
        }

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
        data, total = await gallery_repository.get_all_for_user(db, user_id, page, limit, options)
        total_pages = math.ceil(total / limit) if limit else 0
        return {
            'data': data,
            'meta': {
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            },
        }

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
