from datetime import datetime

from app.schemas.base import CamelBase, CamelOrmSchema


class IdsDto(CamelBase):
    ids: list[str]


class ImageResponse(CamelOrmSchema):
    id: str
    path: str
    original_filename: str
    gallery_id: str
    created_at: datetime


class DeletedImagesResponse(CamelBase):
    deleted: list[str]


class ImageListResponse(CamelBase):
    items: dict[str, list[ImageResponse]]
    page: int
    limit: int
    total: int
    total_pages: int
