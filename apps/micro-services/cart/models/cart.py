"""
models/cart.py ─ Shopping-cart tables (one cart per user).
"""

from cart.extensions import db


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )

    # ─── Relationships ──────────────────────────────────────
    user = db.relationship("User", back_populates="cart")
    items = db.relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )

    # ─── Helpers ────────────────────────────────────────────
    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

    def __repr__(self) -> str:
        return f"<Cart user_id={self.user_id} items={self.item_count}>"


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    # ─── Relationships ──────────────────────────────────────
    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product", back_populates="cart_items")

    # ─── Helpers ────────────────────────────────────────────
    @property
    def subtotal(self) -> float:
        return self.product.price * self.quantity

    def __repr__(self) -> str:
        return f"<CartItem product={self.product.name} qty={self.quantity}>"
