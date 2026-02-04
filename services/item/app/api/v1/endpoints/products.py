"""
Product Endpoints
"""

import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from item.app.core.security.auth import get_current_active_admin
from item.app.db.database import get_db
from item.app.models.product import Category, Product
from item.app.schemas.product import ProductCreate, ProductListResponse, ProductResponse

router = APIRouter()


@router.get("", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all products with pagination"""
    query = db.query(Product).filter(Product.is_active == True)

    if category_id:
        query = query.filter(Product.categories.any(id=category_id))

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    total = query.count()
    total_pages = math.ceil(total / page_size)

    products = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    """Create new product (Admin only)"""
    new_product = Product(**product_data.dict(exclude={"category_ids"}))

    # Add categories
    if product_data.category_ids:
        categories = (
            db.query(Category).filter(Category.id.in_(product_data.category_ids)).all()
        )
        new_product.categories = categories

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
