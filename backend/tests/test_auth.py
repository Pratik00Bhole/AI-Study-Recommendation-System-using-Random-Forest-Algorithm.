from uuid import uuid4

from app import create_app


def _client():
    app = create_app()
    return app.test_client()


def test_signup_requires_fields():
    client = _client()
    response = client.post("/api/auth/signup", json={"email": "a@b.com"})
    assert response.status_code == 400


def test_signup_and_login_success():
    client = _client()
    email = f"user-{uuid4().hex[:8]}@example.com"

    signup_response = client.post(
        "/api/auth/signup",
        json={
            "name": "Test User",
            "email": email,
            "standard": 10,
            "password": "Password123!",
        },
    )

    assert signup_response.status_code == 201
    signup_payload = signup_response.get_json()
    assert signup_payload.get("token")

    login_response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "Password123!"},
    )

    assert login_response.status_code == 200
    login_payload = login_response.get_json()
    assert login_payload.get("token")
    assert login_payload["user"]["email"] == email


def test_validate_token_requires_valid_jwt():
    client = _client()

    unauthorized = client.get("/api/auth/validate")
    assert unauthorized.status_code in {401, 422}

    email = f"user-{uuid4().hex[:8]}@example.com"
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "name": "Validate User",
            "email": email,
            "standard": 10,
            "password": "Password123!",
        },
    )
    token = signup_response.get_json()["token"]

    authorized = client.get(
        "/api/auth/validate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert authorized.status_code == 200
    payload = authorized.get_json()
    assert payload["status"] == "valid"
    assert payload["user_id"]
