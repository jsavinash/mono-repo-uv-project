"""
seed.py ─ Populates the database with sample categories and products.
Runs automatically inside create_app(); is idempotent (skips if data exists).
"""

from cart.extensions import db
from cart.models.product import Category, Product
from cart.utils import slugify

CATEGORIES = [
    {"name": "Electronics", "description": "Gadgets, gizmos & more"},
    {"name": "Clothing", "description": "Apparel for every occasion"},
    {"name": "Home & Garden", "description": "Make your space shine"},
    {"name": "Books", "description": "Expand your mind"},
    {"name": "Sports", "description": "Stay active, stay healthy"},
]

PRODUCTS = [
    # Electronics
    {"name": "Wireless Noise-Cancelling Headphones", "category": "Electronics", "price": 249.99, "stock": 42, "description": "Premium audio with adaptive noise cancellation and 30-hour battery life."},
    {"name": "Ultra HD Smart TV 55\"", "category": "Electronics", "price": 599.99, "stock": 15, "description": "Crystal-clear 4K display with built-in streaming apps and voice control."},
    {"name": "Portable Bluetooth Speaker", "category": "Electronics", "price": 79.99, "stock": 88, "description": "Waterproof 360° sound. Perfect for outdoors."},
    {"name": "Mechanical Keyboard", "category": "Electronics", "price": 129.99, "stock": 55, "description": "RGB backlit with tactile switches. Built for speed and precision."},
    {"name": "Smartwatch Pro", "category": "Electronics", "price": 349.99, "stock": 30, "description": "Track health, fitness, and notifications in style."},
    # Clothing
    {"name": "Classic Cotton T-Shirt", "category": "Clothing", "price": 29.99, "stock": 200, "description": "Soft, breathable 100% organic cotton. Available in 5 colors."},
    {"name": "Slim Fit Chinos", "category": "Clothing", "price": 59.99, "stock": 120, "description": "Versatile chinos that go from office to casual effortlessly."},
    {"name": "Waterproof Hiking Jacket", "category": "Clothing", "price": 149.99, "stock": 40, "description": "Lightweight and breathable. Keeps you dry on the trail."},
    {"name": "Running Shoes X1", "category": "Clothing", "price": 99.99, "stock": 75, "description": "Engineered for speed. Responsive cushioning and breathable mesh."},
    # Home & Garden
    {"name": "Ceramic Plant Pot Set", "category": "Home & Garden", "price": 39.99, "stock": 100, "description": "Handcrafted set of 3 minimalist ceramic pots with drainage holes."},
    {"name": "LED Desk Lamp", "category": "Home & Garden", "price": 44.99, "stock": 60, "description": "Adjustable brightness and color temperature. USB charging port included."},
    {"name": "Scented Soy Candle Bundle", "category": "Home & Garden", "price": 34.99, "stock": 150, "description": "Pack of 6 hand-poured soy candles. 40-hour burn time each."},
    # Books
    {"name": "The Art of Clean Code", "category": "Books", "price": 44.99, "stock": 90, "description": "A deep dive into writing maintainable, readable, and elegant software."},
    {"name": "Sapiens: A Brief History", "category": "Books", "price": 19.99, "stock": 110, "description": "Trace the epic story of humanity from the Stone Age to the present."},
    {"name": "Design Patterns Handbook", "category": "Books", "price": 52.99, "stock": 45, "description": "The go-to reference for software design patterns and best practices."},
    # Sports
    {"name": "Yoga Mat Premium", "category": "Sports", "price": 49.99, "stock": 80, "description": "Extra-thick, non-slip eco-friendly yoga mat with carrying strap."},
    {"name": "Adjustable Dumbbells", "category": "Sports", "price": 199.99, "stock": 25, "description": "5–52.5 lbs per dumbbell. Replaces 15 sets of weights."},
    {"name": "Basketball Official Size", "category": "Sports", "price": 29.99, "stock": 60, "description": "Regulation size and weight. Indoor/outdoor composite leather."},
]


def seed_db() -> None:
    """Insert seed data. Skips entirely if categories already exist."""
    if Category.query.first():
        return  # Already seeded

    # ─── Categories ─────────────────────────────────────────
    cat_map: dict[str, Category] = {}
    for c in CATEGORIES:
        cat = Category(name=c["name"], slug=slugify(c["name"]), description=c["description"])
        db.session.add(cat)
        cat_map[c["name"]] = cat

    db.session.flush()  # Assign IDs to categories before products

    # ─── Products ───────────────────────────────────────────
    for p in PRODUCTS:
        product = Product(
            name=p["name"],
            slug=slugify(p["name"]),
            description=p["description"],
            price=p["price"],
            stock=p["stock"],
            category_id=cat_map[p["category"]].id,
            is_active=True,
        )
        db.session.add(product)

    db.session.commit()
    print("✅ Database seeded with categories and products.")
