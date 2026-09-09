# tests/test_health.py
def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to the Job Board API!'}