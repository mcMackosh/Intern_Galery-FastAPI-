import math
import shutil
import uuid
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.consts.file_managment import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, UPLOAD_ROOT
from app.repositories.image import image_repository

MAX_FILES = 20
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB


class ImageService:
    def _get_gallery_folder(self, gallery_id: str) -> Path:
        folder = UPLOAD_ROOT / gallery_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder
    
    async def upload_images(
        self, db: AsyncSession, gallery_id: str, files: list[UploadFile]
    ):
        if len(files) > MAX_FILES:
            raise HTTPException(
                status_code=400,
                detail=f"Too many files. Maximum {MAX_FILES} allowed per upload",
            )

        validated: list[tuple[UploadFile, bytes]] = []
        for file in files:
            ext = Path(file.filename or "").suffix.lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' has unsupported extension",
                )
            if file.content_type not in ALLOWED_MIME_TYPES:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' has unsupported MIME type",
                )
            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' exceeds the 15 MB size limit",
                )
            validated.append((file, content))

        folder = self._get_gallery_folder(gallery_id)
        created = []

        for file, content in validated:
            filename_safe = file.filename or "unknown"
            file_id = str(uuid.uuid4())
            filename = f"{file_id}_{file.filename}"
            relative_path = f"{gallery_id}/{filename}"
            full_path = folder / filename

            async with aiofiles.open(full_path, "wb") as f:
                await f.write(content)

            image = await image_repository.create(db, gallery_id, relative_path, filename_safe)
            created.append(image)

        await db.commit()
        for image in created:
            await db.refresh(image)

        return created

    async def get_images_by_gallery(
        self, db: AsyncSession, gallery_id: str, page: int, limit: int, order: str
    ):
        items, total = await image_repository.get_by_gallery(db, gallery_id, page, limit, order)
        grouped: dict = {}

        for item in items:
            key = item.created_at.date().isoformat()
            grouped.setdefault(key, []).append(item)

        return {
            'items': grouped,
            'page': page,
            'limit': limit,
            'total': total,
            'total_pages': math.ceil(total / limit) if limit else 0,
        }

    async def delete_images(self, db: AsyncSession, ids: list[str], gallery_id: str):
        images = await image_repository.get_by_ids_and_gallery(db, ids, gallery_id)

        if len(images) != len(ids):
            raise HTTPException(
                status_code=403, detail="Some images do not belong to this gallery"
            )

        await image_repository.delete_many(db, ids)
        await db.commit()

        for image in images:
            path = UPLOAD_ROOT / image.path
            if path.exists():
                path.unlink()

        return {"deleted": ids}

    async def move_images(
        self, db: AsyncSession, ids: list[str], gallery_id: str, target_gallery_id: str
    ):
        images = await image_repository.get_by_ids_and_gallery(db, ids, gallery_id)

        if len(images) != len(ids):
            raise HTTPException(
                status_code=403, detail="Some images do not belong to this gallery"
            )

        target_folder = self._get_gallery_folder(target_gallery_id)

        for image in images:
            filename = Path(image.path).name
            new_relative = f'{target_gallery_id}/{filename}'
            shutil.move(str(UPLOAD_ROOT / image.path), str(target_folder / filename))
            await image_repository.update_gallery(db, image, target_gallery_id, new_relative)

        await db.commit()
        return images

    async def copy_images(
        self, db: AsyncSession, ids: list[str], gallery_id: str, target_gallery_id: str
    ):
        images = await image_repository.get_by_ids_and_gallery(db, ids, gallery_id)

        if len(images) != len(ids):
            raise HTTPException(
                status_code=403, detail="Some images do not belong to this gallery"
            )

        target_folder = self._get_gallery_folder(target_gallery_id)
        created = []

        for image in images:
            file_id = str(uuid.uuid4())
            filename = f'{file_id}_{image.original_filename}'
            new_relative = f'{target_gallery_id}/{filename}'
            shutil.copy2(str(UPLOAD_ROOT / image.path), str(target_folder / filename))
            new_image = await image_repository.create(
                db, target_gallery_id, new_relative, image.original_filename
            )
            created.append(new_image)

        await db.commit()
        for image in created:
            await db.refresh(image)

        return created


image_service = ImageService()
