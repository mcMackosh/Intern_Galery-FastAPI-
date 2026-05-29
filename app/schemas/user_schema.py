from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class LoginDto(BaseModel):
    email: str
    password: str = Field(min_length=8)

class RegisterDto(BaseModel):
    first_name: str = Field(min_length=4, max_length=20)
    last_name: str = Field(min_length=4, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*]", value):
            raise ValueError("Password must contain a special character: !@#$%^&*")
        return value

class UserResponce(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    
    model_config = {"from_attributes": True}

