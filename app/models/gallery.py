import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.membership import Membership


class Gallery(Base, TimestampMixin):
    __tablename__ = "galleries"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    memberships: Mapped[list["Membership"]] = relationship(
        "Membership", back_populates="gallery", cascade="all, delete-orphan"
    )