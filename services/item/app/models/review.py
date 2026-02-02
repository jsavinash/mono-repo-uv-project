"""
Review Model
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from item.app.db.database import Base


class Review(Base):
    """Product Review model"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))  # Optional: link to purchase
    
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String)
    comment = Column(Text)
    
    is_verified_purchase = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    
    helpful_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review {self.id} - {self.rating} stars>"
