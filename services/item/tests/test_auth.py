"""
Test User Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.db.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAuth:
    """Test authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPass123",
                "first_name": "Test",
                "last_name": "User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "username": "user1",
                "password": "TestPass123"
            }
        )
        
        # Duplicate registration
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "username": "user2",
                "password": "TestPass123"
            }
        )
        assert response.status_code == 400
    
    def test_login_success(self):
        """Test successful login"""
        # Register user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "username": "loginuser",
                "password": "TestPass123"
            }
        )
        
        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "TestPass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "WrongPass123"
            }
        )
        assert response.status_code == 401


class TestProducts:
    """Test product endpoints"""
    
    def test_get_products(self):
        """Test getting products"""
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data


# Cleanup after tests
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup test database after all tests"""
    def remove_test_db():
        import os
        if os.path.exists("test.db"):
            os.remove("test.db")
    
    request.addfinalizer(remove_test_db)
