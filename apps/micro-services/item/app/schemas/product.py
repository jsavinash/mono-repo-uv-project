"""
Product Schemas
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class CategoryBase(BaseModel):
    """Base category schema"""

    name: str
    slug: str
    description: str | None = None
    parent_id: int | None = None


class CategoryCreate(CategoryBase):
    """Schema for creating category"""


class CategoryResponse(CategoryBase):
    """Schema for category response"""

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProductImageBase(BaseModel):
    """Base product image schema"""

    image_url: str
    alt_text: str | None = None
    is_primary: bool = False


class ProductImageResponse(ProductImageBase):
    """Schema for product image response"""

    id: int
    display_order: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base product schema"""

    name: str = Field(..., min_length=1, max_length=200)
    slug: str
    description: str | None = None
    short_description: str | None = None
    sku: str
    price: float = Field(..., gt=0)
    compare_price: float | None = None
    stock_quantity: int = Field(..., ge=0)
    brand: str | None = None


class ProductCreate(ProductBase):
    """Schema for creating product"""

    category_ids: list[int] = []

    @validator("compare_price")
    def validate_compare_price(cls, v, values):
        if v is not None and "price" in values and v < values["price"]:
            raise ValueError("Compare price must be greater than selling price")
        return v


class ProductUpdate(BaseModel):
    """Schema for updating product"""

    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    stock_quantity: int | None = Field(None, ge=0)
    is_active: bool | None = None


class ProductResponse(ProductBase):
    """Schema for product response"""

    id: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime
    categories: list[CategoryResponse] = []
    images: list[ProductImageResponse] = []

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for paginated product list"""

    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
