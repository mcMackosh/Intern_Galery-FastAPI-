from datetime import datetime
from pydantic import EmailStr, Field, field_validator
import re

from app.schemas.base import CamelBase, CamelOrmSchema


class LoginDto(CamelBase):
    email: str
    password: str = Field(min_length=6)


class RegisterDto(CamelBase):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator('first_name', 'last_name')
    @classmethod
    def letters_only(cls, value: str) -> str:
        if not re.match(r'^[A-Za-zА-ЯҐЄІЇа-яґєії\'\- ]+$', value):
            raise ValueError("Must contain only letters")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        return value


class UpdateProfileDto(CamelBase):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def letters_only(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not re.match(r'^[A-Za-zА-ЯҐЄІЇа-яґєії\'\- ]+$', value):
            raise ValueError("Must contain only letters")
        return value


class ChangePasswordDto(CamelBase):
    old_password: str
    new_password: str = Field(min_length=6)


class AccessTokenResponse(CamelBase):
    access_token: str


class UserResponse(CamelOrmSchema):
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime


UserResponce = UserResponse
