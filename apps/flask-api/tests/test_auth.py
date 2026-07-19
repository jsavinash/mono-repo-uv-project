def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert "access_token" in data


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "user1",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user2",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    assert response.status_code == 409


def test_login_success(client):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    # Then login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401
