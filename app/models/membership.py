import enum
import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, TimestampMixin
from app.models.gallery import Gallery
from app.models.user import User

class UserRole(str, enum.Enum):
    REGULAR = "REGULAR"
    ADMIN = "ADMIN"
    OWNER = "OWNER"
    
class Membership(Base, TimestampMixin):
    __tablename__ = 'memberships'
    
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey('user.id', ondelete='CASCADE'), nullable=False
    )
    
    gallery_id: Mapped[str] = mapped_column(
        String, ForeignKey('gallery.id', ondelete='CASCADE'), nullable=False
    )
    
    role: Mapped[UserRole] = mapped_column(
        String, nullable=False, default=UserRole.REGULAR
    )
    
    user: Mapped["User"] = relationship("User", back_populates="memberships")
    gallery: Mapped["Gallery"] = relationship("Gallery", back_populates="memberships")
    
