"""
Order Endpoints
"""

from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from item.app.core.security.auth import get_current_user
from item.app.db.database import get_db
from item.app.models.order import CartItem, Order, OrderItem, OrderStatus
from item.app.models.user import User
from item.app.schemas.order import OrderCreate, OrderResponse

router = APIRouter()


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create new order from cart"""
    # Get cart items
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate totals
    subtotal = 0
    order_items = []

    for cart_item in cart_items:
        product = cart_item.product

        # Check stock
        if product.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for {product.name}"
            )

        item_total = product.price * cart_item.quantity
        subtotal += item_total

        order_items.append(
            {
                "product_id": product.id,
                "quantity": cart_item.quantity,
                "price": product.price,
                "total": item_total,
            }
        )

        # Update stock
        product.stock_quantity -= cart_item.quantity

    # Calculate tax and total
    tax = subtotal * 0.18  # 18% tax
    shipping_cost = 50 if subtotal < 500 else 0  # Free shipping above 500
    total = subtotal + tax + shipping_cost

    # Create order
    new_order = Order(
        order_number=f"ORD-{uuid.uuid4().hex[:12].upper()}",
        user_id=current_user.id,
        status=OrderStatus.PENDING,
        subtotal=subtotal,
        tax=tax,
        shipping_cost=shipping_cost,
        total=total,
        shipping_address_id=order_data.shipping_address_id,
        billing_address_id=order_data.billing_address_id
        or order_data.shipping_address_id,
        payment_method=order_data.payment_method,
        notes=order_data.notes,
    )
    db.add(new_order)
    db.flush()

    # Create order items
    for item_data in order_items:
        order_item = OrderItem(order_id=new_order.id, **item_data)
        db.add(order_item)

    # Clear cart
    for cart_item in cart_items:
        db.delete(cart_item)

    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("", response_model=List[OrderResponse])
async def get_my_orders(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user's orders"""
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get specific order"""
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == current_user.id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
