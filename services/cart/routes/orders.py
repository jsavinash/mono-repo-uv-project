"""
routes/orders.py ─ Checkout, payment (Stripe stub), and order history.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from cart.extensions import db
from cart.forms.checkout import CheckoutForm
from cart.models.order import Order, OrderItem, OrderStatus

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = current_user.cart
    if not cart or not cart.items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("main.index"))

    form = CheckoutForm()

    # Pre-fill with user info on GET
    if request.method == "GET":
        form.shipping_name.data = current_user.full_name
        form.shipping_email.data = current_user.email

    if form.validate_on_submit():
        # ─── Create order ───────────────────────────────────
        order = Order(
            user_id=current_user.id,
            status=OrderStatus.PENDING,
            total=cart.total,
            shipping_name=form.shipping_name.data,
            shipping_email=form.shipping_email.data,
            shipping_address=form.shipping_address.data,
            shipping_city=form.shipping_city.data,
            shipping_state=form.shipping_state.data,
            shipping_zip=form.shipping_zip.data,
            shipping_country=form.shipping_country.data,
        )
        db.session.add(order)
        db.session.flush()  # Get the order ID

        # ─── Snapshot line items & decrement stock ──────────
        for cart_item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
            )
            db.session.add(order_item)
            cart_item.product.stock -= cart_item.quantity

        # ─── Clear cart ─────────────────────────────────────
        for item in cart.items:
            db.session.delete(item)

        # ─── Mark paid (Stripe integration point) ──────────
        # In production, you would create a Stripe PaymentIntent here
        # and redirect to a payment confirmation page.
        # For now, we simulate immediate payment success.
        order.status = OrderStatus.PAID

        db.session.commit()

        flash(f"Order #{order.id} placed successfully! 🎉", "success")
        return redirect(url_for("orders.order_detail", order_id=order.id))

    return render_template(
        "orders/checkout.html",
        form=form,
        cart=cart,
        stripe_publishable_key=current_app_config("STRIPE_PUBLISHABLE_KEY"),
    )


@orders_bp.route("/history")
@login_required
def history():
    orders = current_user.orders
    return render_template("orders/history.html", orders=orders)


@orders_bp.route("/<int:order_id>")
@login_required
def order_detail(order_id: int):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash("You don't have permission to view this order.", "error")
        return redirect(url_for("orders.history"))
    return render_template("orders/detail.html", order=order)


# ─── Helper ─────────────────────────────────────────────────────
def current_app_config(key: str):
    from flask import current_app
    return current_app.config.get(key, "")
