import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.gallery import Gallery


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
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    gallery_id: Mapped[str] = mapped_column(
        String, ForeignKey("galleries.id", ondelete="CASCADE"), nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        String, nullable=False, default=UserRole.REGULAR
    )

    user: Mapped["User"] = relationship("User", back_populates="memberships")
    gallery: Mapped["Gallery"] = relationship("Gallery", back_populates="memberships")
