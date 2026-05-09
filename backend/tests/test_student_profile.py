from uuid import uuid4

from app import create_app


def _auth_headers(client):
    email = f"student-{uuid4().hex[:8]}@example.com"
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "name": "Student User",
            "email": email,
            "standard": 11,
            "password": "Password123!",
        },
    )
    token = signup_response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_save_and_get_profile():
    app = create_app()
    client = app.test_client()
    headers = _auth_headers(client)

    payload = {
        "student_details": {"name": "Student User", "class": "11"},
        "subjects": [
            {"name": "Math", "marks": 72, "level": "average"},
            {"name": "Physics", "marks": 48, "level": "low"},
        ],
        "skills": ["problem solving"],
        "interests": ["engineering"],
    }

    save_response = client.post("/api/student/profile", json=payload, headers=headers)
    assert save_response.status_code == 200
    assert save_response.get_json().get("analysis") is not None

    get_response = client.get("/api/student/profile", headers=headers)
    assert get_response.status_code == 200
    profile = get_response.get_json().get("profile")
    assert profile is not None
    assert profile.get("marks", {}).get("Math") == 72.0
