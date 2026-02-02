"""
models/order.py ─ Order & line-item tables.
"""

from datetime import datetime

from cart.extensions import db


class OrderStatus:
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    CHOICES = [PENDING, PAID, SHIPPED, DELIVERED, CANCELLED]


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default=OrderStatus.PENDING, nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    # ─── Shipping address ───────────────────────────────────
    shipping_name = db.Column(db.String(150), default="")
    shipping_email = db.Column(db.String(150), default="")
    shipping_address = db.Column(db.String(300), default="")
    shipping_city = db.Column(db.String(100), default="")
    shipping_state = db.Column(db.String(100), default="")
    shipping_zip = db.Column(db.String(20), default="")
    shipping_country = db.Column(db.String(100), default="US")

    # ─── Payment ────────────────────────────────────────────
    stripe_payment_intent_id = db.Column(db.String(100), default="")
    stripe_client_secret = db.Column(db.String(200), default="")

    # ─── Timestamps ─────────────────────────────────────────
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ─── Relationships ──────────────────────────────────────
    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @property
    def total_display(self) -> str:
        return f"${self.total:.2f}"

    def __repr__(self) -> str:
        return f"<Order #{self.id} status={self.status} total={self.total}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)  # Snapshot of price at time of purchase

    # ─── Relationships ──────────────────────────────────────
    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")

    @property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity

    def __repr__(self) -> str:
        return f"<OrderItem product={self.product.name} qty={self.quantity}>"
