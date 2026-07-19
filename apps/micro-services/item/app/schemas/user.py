"""
User Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import Optional

from item.app.models.user import UserRole
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class UserCreate(UserBase):
    """Schema for user registration"""

    password: str = Field(..., min_length=8)

    @validator("password")
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v


class UserUpdate(BaseModel):
    """Schema for user update"""

    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response"""

    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: datetime | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""

    user_id: int | None = None
    email: str | None = None
