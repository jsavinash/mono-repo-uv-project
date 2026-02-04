"""
Shopping Cart Endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from item.app.core.security.auth import get_current_user
from item.app.db.database import get_db
from item.app.models.order import CartItem
from item.app.models.product import Product
from item.app.models.user import User
from item.app.schemas.order import CartItemCreate, CartItemResponse

router = APIRouter()


@router.get("", response_model=List[CartItemResponse])
async def get_cart(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user's cart items"""
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    return cart_items


@router.post("", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    cart_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add item to cart"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == cart_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity < cart_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Check if item already in cart
    existing_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == cart_data.product_id,
        )
        .first()
    )

    if existing_item:
        existing_item.quantity += cart_data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    # Create new cart item
    new_item = CartItem(
        user_id=current_user.id,
        product_id=cart_data.product_id,
        quantity=cart_data.quantity,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.delete("/{cart_item_id}")
async def remove_from_cart(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove item from cart"""
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.id == cart_item_id, CartItem.user_id == current_user.id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "Item removed from cart"}
