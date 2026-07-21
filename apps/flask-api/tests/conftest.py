import pytest
from src.app import create_app
from src.extensions import db as _db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Get database instance."""
    with app.app_context():
        yield _db
        _db.session.rollback()
        _db.drop_all()
        _db.create_all()
