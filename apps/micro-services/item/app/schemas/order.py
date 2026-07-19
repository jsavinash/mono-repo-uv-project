"""
Order and Cart Schemas
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from item.app.models.order import OrderStatus, PaymentStatus


class AddressBase(BaseModel):
    """Base address schema"""

    full_name: str
    phone_number: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "India"
    is_default: bool = False


class AddressCreate(AddressBase):
    """Schema for creating address"""

    pass


class AddressResponse(AddressBase):
    """Schema for address response"""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CartItemBase(BaseModel):
    """Base cart item schema"""

    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    """Schema for adding to cart"""

    pass


class CartItemUpdate(BaseModel):
    """Schema for updating cart item"""

    quantity: int = Field(..., gt=0)


class CartItemResponse(CartItemBase):
    """Schema for cart item response"""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    """Base order item schema"""

    product_id: int
    quantity: int = Field(..., gt=0)
    price: float


class OrderItemResponse(OrderItemBase):
    """Schema for order item response"""

    id: int
    total: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating order"""

    shipping_address_id: int
    billing_address_id: Optional[int] = None
    payment_method: str
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    """Schema for order response"""

    id: int
    order_number: str
    status: OrderStatus
    payment_status: PaymentStatus
    subtotal: float
    tax: float
    shipping_cost: float
    discount: float
    total: float
    created_at: datetime
    items: List[OrderItemResponse] = []
    shipping_address: Optional[AddressResponse] = None

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Schema for paginated order list"""

    items: List[OrderResponse]
    total: int
    page: int
    page_size: int
