"""
routes/cart.py ─ Shopping cart CRUD.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from cart.extensions import db
from cart.models.cart import Cart, CartItem
from cart.models.product import Product

cart_bp = Blueprint("cart", __name__)


def _get_or_create_cart() -> Cart:
    """Return the current user's cart, creating one if needed."""
    if current_user.cart is None:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    return current_user.cart


@cart_bp.route("/")
@login_required
def view_cart():
    cart = _get_or_create_cart()
    return render_template("cart/view.html", cart=cart)


@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_item(product_id: int):
    product = Product.query.get_or_404(product_id)

    if not product.in_stock:
        flash("Sorry, this product is out of stock.", "error")
        return redirect(request.referrer or url_for("products.listing"))

    cart = _get_or_create_cart()
    existing = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()

    if existing:
        if existing.quantity < product.stock:
            existing.quantity += 1
        else:
            flash("Maximum stock quantity reached.", "warning")
    else:
        item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
        db.session.add(item)

    db.session.commit()
    flash(f"{product.name} added to cart!", "success")
    return redirect(request.referrer or url_for("cart.view_cart"))


@cart_bp.route("/update/<int:item_id>", methods=["POST"])
@login_required
def update_item(item_id: int):
    item = CartItem.query.get_or_404(item_id)
    quantity = request.form.get("quantity", 1, type=int)

    if quantity < 1:
        db.session.delete(item)
    elif quantity > item.product.stock:
        flash(f"Only {item.product.stock} available.", "warning")
        return redirect(url_for("cart.view_cart"))
    else:
        item.quantity = quantity

    db.session.commit()
    flash("Cart updated.", "success")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_item(item_id: int):
    item = CartItem.query.get_or_404(item_id)
    product_name = item.product.name
    db.session.delete(item)
    db.session.commit()
    flash(f"{product_name} removed from cart.", "success")
    return redirect(url_for("cart.view_cart"))
