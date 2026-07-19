from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def admin_client(api_client):
    admin = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
    )
    api_client.force_authenticate(user=admin)
    return api_client, admin
