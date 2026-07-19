import pytest
from rest_framework import status


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_endpoint(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.status_code == status.HTTP_200_OK
