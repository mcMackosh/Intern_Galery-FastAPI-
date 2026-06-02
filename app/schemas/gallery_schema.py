from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class CreateGalleryDto(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str | None = Field(default=None, min_length=3, max_length=250)
    
    @field_validator('description')
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value
    
    
class UpdateGalleryDto(CreateGalleryDto): 
    pass

class GetGalleriesQueryDto(BaseModel):
    search: str | None = None
    sort_by: Literal['createdAt', 'title'] | None = None
    order_by: Literal['asc', 'desc'] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    min_images: int | None = None
    max_images: int | None = None