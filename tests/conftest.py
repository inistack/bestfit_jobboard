# tests/conftest.py
import pytest
from jobboard import create_app
from jobboard.extensions import db as _db


@pytest.fixture
def app():
    app = create_app('config.TestingConfig')

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def candidate_token(client):
    client.post('/auth/register', json={
        'email': 'candidate@test.com',
        'name': 'Test Candidate',
        'password': 'password123',
        'role': 'candidate',
    })
    response = client.post('/auth/login', json={
        'email': 'candidate@test.com',
        'password': 'password123',
    })
    return response.json['access_token']


@pytest.fixture
def employer_token(client):
    client.post('/auth/register', json={
        'email': 'employer@test.com',
        'name': 'Test Employer',
        'password': 'password123',
        'role': 'employer',
    })
    response = client.post('/auth/login', json={
        'email': 'employer@test.com',
        'password': 'password123',
    })
    return response.json['access_token']

@pytest.fixture
def auth_header():
    def _auth_header(token):
        return {'Authorization': f'Bearer {token}'}
    return _auth_header