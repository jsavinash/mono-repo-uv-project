from typing import Any
import uuid


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())


def paginate(query, page: int = 1, per_page: int = 25):
    """Paginate a SQLAlchemy query."""
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": pagination.items,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    }
