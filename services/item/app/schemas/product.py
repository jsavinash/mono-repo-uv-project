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
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """Schema for creating category"""

    pass


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
    alt_text: Optional[str] = None
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
    description: Optional[str] = None
    short_description: Optional[str] = None
    sku: str
    price: float = Field(..., gt=0)
    compare_price: Optional[float] = None
    stock_quantity: int = Field(..., ge=0)
    brand: Optional[str] = None


class ProductCreate(ProductBase):
    """Schema for creating product"""

    category_ids: List[int] = []

    @validator("compare_price")
    def validate_compare_price(cls, v, values):
        if v is not None and "price" in values and v < values["price"]:
            raise ValueError("Compare price must be greater than selling price")
        return v


class ProductUpdate(BaseModel):
    """Schema for updating product"""

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response"""

    id: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryResponse] = []
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for paginated product list"""

    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
