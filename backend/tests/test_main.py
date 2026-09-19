from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_init_database_rejects_invalid_api_key():
    response = client.post("/init-db", json={"key": "wrong-key"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized: Invalid API key provided."


def test_private_endpoint_requires_a_session():
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_signup_rejects_short_password_before_database_access():
    response = client.post(
        "/auth/signup",
        json={"email": "user@example.com", "password": "short", "name": "User"},
    )

    assert response.status_code == 422
