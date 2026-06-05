from datetime import datetime
from typing import Literal
from pydantic import Field, field_validator

from app.schemas.base import CamelBase, CamelOrmSchema


class CreateGalleryDto(CamelBase):
    title: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, min_length=10, max_length=255)

    @field_validator('description')
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value


class UpdateGalleryDto(CreateGalleryDto):
    pass


class GetGalleriesQueryDto(CamelBase):
    search: str | None = None
    sort_by: Literal['createdAt', 'title'] | None = None
    order_by: Literal['asc', 'desc'] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    min_images: int | None = None
    max_images: int | None = None


class GalleryResponse(CamelOrmSchema):
    id: str
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class GalleryDetailResponse(CamelBase):
    id: str
    title: str
    created_at: datetime
    role: str | None = None


class GalleryListItemResponse(CamelBase):
    id: str
    title: str
    created_at: datetime
    role: str | None
    images_count: int
    images: list[str]


class GalleriesMetaResponse(CamelBase):
    total: int
    page: int
    limit: int
    total_pages: int


class GalleriesListResponse(CamelBase):
    data: list[GalleryListItemResponse]
    meta: GalleriesMetaResponse
