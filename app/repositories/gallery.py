from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gallery import Gallery
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
    ) -> list[Gallery]:
        
        query = (
            select(Gallery).
            join(Membership, Membership.gallery_id == Gallery.id).
            where(Membership.user_id == user_id)
        )
        
        if options.search:
            query = query.where(Gallery.title.ilike(f"%{options.search}%"))
            
        if options.start_date:
            query = query.where(Gallery.created_at >= options.start_date)
        
        if options.end_date:
            query = query.where(Gallery.created_at <= options.end_date)
        
        if options.sort_by == 'title':
            order_col = Gallery.title
        else:
            order_col = Gallery.created_at
            
        query = query.order_by(
            order_col.asc() if options.order_by == 'asc' else order_col.desc()
        )
        
        query = query.offset((page - 1) * limit).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
        
        
gallery_repository = GalleryRepository()