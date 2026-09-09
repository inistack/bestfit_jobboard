def test_register_success(client):
    response = client.post('/auth/register', json={
        'email': 'candidate1@gmail.com',
        'name': 'Candidate One',
        'password': 'password123',
        'role': 'candidate'}
    )
    assert response.status_code == 201
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json


def test_register_existing_email(client):
    response = client.post(
        '/auth/register', json={
            'email': 'candidate2@gmail.com',
            'name': 'Candidate Two',
            'password': 'password123',
            'role': 'candidate'
        }
    )
    assert response.status_code == 201

    response = client.post(
        '/auth/register', json={
            'email': 'candidate2@gmail.com',
            'name': 'Candidate Two',
            'password': 'password123',
            'role': 'candidate'
        }
    )
    assert response.status_code == 409


def test_register_invalid_role(client):
    response = client.post(
        '/auth/register', json={
            'email': 'candidate3@gmail.com',
            'name': 'Candidate Three',
            'password': 'password123',
            'role': 'admin'
        }
    )
    assert response.status_code == 422


def test_login_success(client):
    client.post(
        '/auth/register', json={
            'email': 'candidate4@gmail.com',
            'name': 'Candidate Four',
            'password': 'password123',
            'role': 'candidate'
        }
    )
    response = client.post(
        '/auth/login', json={
            'email': 'candidate4@gmail.com',
            'password': 'password123'
        }
    )
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json


def test_login_wrong_password(client):
    client.post(
        '/auth/register', json={
            'email': 'candidate5@gmail.com',
            'name': 'Candidate Five',
            'password': 'password123',
            'role': 'candidate'
        }
    )
    response = client.post(
        '/auth/login', json={
            'email': 'candidate5@gmail.com',
            'password': 'wrongpassword'
        }
    )
    assert response.status_code == 401


def test_login_nonexistent_email(client):
    response = client.post(
        '/auth/login', json={
            'email': 'nonexistent@gmail.com',
            'password': 'password123',
        }
    )
    assert response.status_code == 401


