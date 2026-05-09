from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json.get('status') == 'ok'


def test_readiness_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.get('/api/health/ready')
    assert response.status_code in (200, 503)
    assert response.json.get('status')
