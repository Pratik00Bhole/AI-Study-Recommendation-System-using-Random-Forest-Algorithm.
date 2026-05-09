from unittest.mock import patch
from uuid import uuid4

from app import create_app


def _auth_headers(client):
    email = f"reco-{uuid4().hex[:8]}@example.com"
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "name": "Reco User",
            "email": email,
            "standard": 10,
            "password": "Password123!",
        },
    )
    token = signup_response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_recommendations_requires_profile():
    app = create_app()
    client = app.test_client()
    headers = _auth_headers(client)

    response = client.get("/api/recommendations/", headers=headers)
    assert response.status_code == 404


def test_recommendations_returns_data():
    app = create_app()
    client = app.test_client()
    headers = _auth_headers(client)

    client.post(
        "/api/student/profile",
        json={
            "subjects": [{"name": "Math", "marks": 35, "level": "low"}],
            "skills": ["focus"],
            "interests": ["science"],
        },
        headers=headers,
    )

    with patch(
        "app.routes.recommendation_routes.AIEngineService.detect_topic_strengths",
        return_value={"weak_topics": ["Math"], "strong_topics": []},
    ), patch(
        "app.routes.recommendation_routes.RecommendationService.recommend",
        return_value=[{"topic": "Linear Equations", "score": 0.91}],
    ):
        response = client.get("/api/recommendations/", headers=headers)

    assert response.status_code == 200
    payload = response.get_json()
    assert payload.get("analysis", {}).get("weak_topics") == ["Math"]
    assert len(payload.get("recommendations", [])) == 1
