from collections import defaultdict

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gallery import Gallery
from app.models.image import Image
from app.models.membership import Membership
from app.schemas.gallery_schema import CreateGalleryDto, GetGalleriesQueryDto, UpdateGalleryDto

class GalleryRepository:
    
    async def get_by_id(self, db: AsyncSession, gallery_id: str) -> Gallery | None:
        result = await db.execute(select(Gallery).where(Gallery.id == gallery_id))
        return result.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, dto: CreateGalleryDto) -> Gallery:
        gallery = Gallery(**dto.model_dump())
        db.add(gallery)
        await db.commit()
        await db.refresh(gallery)
        return gallery
    
    async def update(self, db: AsyncSession, gallery: Gallery, dto: UpdateGalleryDto):
        gallery.title = dto.title
        if dto.description is not None:
            gallery.description = dto.description
        
        await db.commit()
        await db.refresh(gallery)
        return gallery
    
    async def delete(self, db: AsyncSession, gallery: Gallery) -> None:
        await db.delete(gallery)
        await db.commit()
        
    async def get_all_for_user(
        self,
        db: AsyncSession,
        user_id: str,
        page: int,
        limit: int,
        options: GetGalleriesQueryDto,
    ) -> tuple[list[dict], int]:

        def _base():
            q = (
                select(
                    Gallery,
                    Membership.role.label('member_role'),
                    func.count(Image.id).label('images_count'),
                )
                .join(Membership, and_(
                    Membership.gallery_id == Gallery.id,
                    Membership.user_id == user_id,
                ))
                .outerjoin(Image, Image.gallery_id == Gallery.id)
                .group_by(Gallery.id, Membership.role)
            )
            if options.search:
                q = q.where(Gallery.title.ilike(f"%{options.search}%"))
            if options.start_date:
                q = q.where(Gallery.created_at >= options.start_date)
            if options.end_date:
                q = q.where(Gallery.created_at <= options.end_date)
            if options.min_images is not None:
                q = q.having(func.count(Image.id) >= options.min_images)
            if options.max_images is not None:
                q = q.having(func.count(Image.id) <= options.max_images)
            return q

        total = (
            await db.execute(select(func.count()).select_from(_base().subquery()))
        ).scalar_one()

        order_col = Gallery.title if options.sort_by == 'title' else Gallery.created_at
        rows = (
            await db.execute(
                _base()
                .order_by(order_col.asc() if options.order_by == 'asc' else order_col.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()

        gallery_ids = [row.Gallery.id for row in rows]
        images_by_gallery: dict[str, list[str]] = defaultdict(list)
        if gallery_ids:
            img_rows = (
                await db.execute(
                    select(Image)
                    .where(Image.gallery_id.in_(gallery_ids))
                    .order_by(Image.created_at.desc())
                )
            ).scalars().all()
            for img in img_rows:
                images_by_gallery[img.gallery_id].append(img.path)

        return [
            {
                'id': row.Gallery.id,
                'title': row.Gallery.title,
                'created_at': row.Gallery.created_at,
                'role': row.member_role,
                'images_count': row.images_count,
                'images': images_by_gallery[row.Gallery.id][:4],
            }
            for row in rows
        ], total


gallery_repository = GalleryRepository()
