"""
routes/main.py ─ Homepage, featured products, and generic pages.
"""

from flask import Blueprint, render_template

from cart.models.product import Category, Product

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage — shows featured (newest) products and all categories."""
    categories = Category.query.all()
    featured = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(8).all()
    return render_template("base/index.html", categories=categories, featured=featured)


@main_bp.route("/about")
def about():
    return render_template("base/about.html")
