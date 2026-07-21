"""Shared DTOs and contracts using Pydantic for cross-service data validation."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class TokenType(str, Enum):
    """JWT token type enumeration."""

    ACCESS = "access"
    REFRESH = "refresh"


# ─── Data Transfer Objects ──────────────────────────────────────


class UserDTO(BaseModel):
    """User data transfer object shared across services."""

    id: str
    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    phone_number: str = ""
    bio: str = ""
    avatar: str = ""
    email_verified: bool = False
    is_active: bool = True
    is_admin: bool = False
    theme: str = "light"
    email_notifications: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserCreateRequest(BaseModel):
    """User creation request payload."""

    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLoginRequest(BaseModel):
    """User login request payload."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""

    items: list[dict[str, Any]]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class ApiResponse(BaseModel):
    """Standard API response wrapper."""

    success: bool = True
    message: str = ""
    data: dict[str, Any] | list[dict[str, Any]] | None = None
    errors: dict[str, Any] | None = None


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class AppFeature:
    """Application feature descriptor."""

    title: str
    description: str


@dataclass(frozen=True)
class ProductPlan:
    """Product plan descriptor."""

    name: str
    price_monthly: int
    description: str