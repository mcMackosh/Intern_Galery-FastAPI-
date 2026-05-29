import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.membership import Membership

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    first_name: Mapped[str]
    
    last_name: Mapped[str]
    
    email: Mapped[str] = mapped_column(
        String, unique=True
    )
    
    hashed_password: Mapped[str]
    
    memberships: Mapped[list["Membership"]] = relationship(
        "Membership", back_populates="user", 
        cascade="all, delete-orphan"
    )
