from django.contrib.auth import get_user_model
import pytest
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user_success(self):
        client = APIClient()
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = client.post("/api/v1/auth/register/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data
        assert "refresh" in response.data
        assert User.objects.count() == 1

    def test_register_user_password_mismatch(self):
        client = APIClient()
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "differentpass",
        }
        response = client.post("/api/v1/auth/register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserAuthentication:
    def test_login_success(self):
        User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        client = APIClient()
        response = client.post(
            "/api/v1/auth/login/",
            {"email": "test@example.com", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_login_invalid_credentials(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/login/",
            {"email": "wrong@example.com", "password": "wrongpass"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
