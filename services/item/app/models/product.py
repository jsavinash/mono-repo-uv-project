"""
Product Model
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from item.app.db.database import Base

# Association table for product categories
product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Product(Base):
    """Product model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    short_description = Column(String(500))
    
    sku = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    compare_price = Column(Float)  # Original price for discount display
    cost_per_item = Column(Float)
    
    stock_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    
    weight = Column(Float)  # in kg
    dimensions = Column(String)  # LxWxH in cm
    
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    brand = Column(String)
    barcode = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = relationship("Category", secondary=product_categories, back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product {self.name}>"


class Category(Base):
    """Category model"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    
    parent_id = Column(Integer, ForeignKey('categories.id'))
    
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", secondary=product_categories, back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    
    def __repr__(self):
        return f"<Category {self.name}>"


class ProductImage(Base):
    """Product Image model"""
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    image_url = Column(String, nullable=False)
    alt_text = Column(String)
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="images")
    
    def __repr__(self):
        return f"<ProductImage {self.id}>"
