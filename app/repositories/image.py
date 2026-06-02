from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image import Image

class ImageRepository:
    async def create(
        self, db: AsyncSession, gallery_id: str, path: str, original_filename: str
    ) -> Image:
        image = Image(path=path, original_filename=original_filename, gallery_id=gallery_id)
        db.add(image)
        return image
    
    async def get_by_ids_and_gallery(
        self, db: AsyncSession, ids: list[str], gallery_id: str
    ) -> list[Image]:
        result = await db.execute(
            select(Image).where(Image.id.in_(ids), Image.gallery_id == gallery_id)
        )
        return list(result.scalars().all())
    
    async def get_by_gallery(
        self,
        db: AsyncSession,
        gallery_id: str,
        page: int,
        limit: int,
        order: str,
    ) -> tuple[list[Image], int]:
        
        query = (
            select(Image)
            .where(Image.gallery_id == gallery_id)
            .order_by(Image.created_at.asc() if order == 'asc' else Image.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        
        count_query = (
            select(Image)
            .where(Image.gallery_id == gallery_id)
        )
        
        items = list((await db.execute(query)).scalars().all())
        total = len((await db.execute(count_query)).scalars().all())
        
        return items, total
    
    async def delete_many(self, db: AsyncSession, ids: list[str]) -> None:
        await db.execute(delete(Image).where(Image.id.in_(ids)))
        
    async def update_gallery(
        self, db: AsyncSession, image: Image, gallery_id: str, new_path: str
    ) -> Image:
        image.gallery_id = gallery_id
        image.path = new_path
        return image
    
image_repository = ImageRepository()