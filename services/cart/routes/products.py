"""
routes/products.py ─ Product listing, detail, and search.
"""

from flask import Blueprint, abort, render_template, request

from cart.models.product import Category, Product

products_bp = Blueprint("products", __name__)


@products_bp.route("/")
def listing():
    """
    Product listing page.
    Supports filtering by ?category=<slug> and searching by ?q=<query>.
    Pagination via ?page=<int>.
    """
    category_slug = request.args.get("category")
    query_text = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Product.query.filter_by(is_active=True)

    # ─── Category filter ────────────────────────────────────
    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first_or_404()
        query = query.filter_by(category_id=selected_category.id)

    # ─── Text search ────────────────────────────────────────
    if query_text:
        pattern = f"%{query_text}%"
        query = query.filter(Product.name.ilike(pattern) | Product.description.ilike(pattern))

    # ─── Sort ───────────────────────────────────────────────
    sort = request.args.get("sort", "newest")
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "name":
        query = query.order_by(Product.name.asc())
    else:  # newest
        query = query.order_by(Product.created_at.desc())

    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()

    return render_template(
        "products/listing.html",
        products=products,
        categories=categories,
        selected_category=selected_category,
        query_text=query_text,
        sort=sort,
    )


@products_bp.route("/<string:slug>")
def detail(slug: str):
    """Single product detail page."""
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    return render_template("products/detail.html", product=product)
