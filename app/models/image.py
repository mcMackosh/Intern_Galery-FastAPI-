import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.gallery import Gallery
    
class Image(Base, TimestampMixin):
    __tablename__ = 'images'
    
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    
    path: Mapped[str] = mapped_column(String, nullable=False)
    
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    
    gallery_id: Mapped[str] = mapped_column(String, ForeignKey('galleries.id', ondelete='CASCADE'), nullable=False)
    
    gallery: Mapped["Gallery"] = relationship("Gallery", back_populates="images")