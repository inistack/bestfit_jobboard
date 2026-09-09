from jobboard import create_app
from jobboard.extensions import db as _db

def test_create_application_triggers_pipeline(client, candidate_token, employer_token, auth_header, mock_celery_chain):
    job_response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    job_id = job_response.json['id']

    response = client.post('/applications',
        json={'job_id': job_id, 'cover_letter': 'I would love this job'},
        headers=auth_header(candidate_token)
    )

    assert response.status_code == 201
    mock_celery_chain.assert_called_once()


def test_create_application(client, candidate_token, employer_token, auth_header):
    client.post(
        '/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    response = client.post(
        '/applications',
        json={'job_id': 1, 'cover_letter': 'I am interested in this position.'},
        headers=auth_header(candidate_token)
    )
    assert response.status_code == 201

def test_get_applications(client, candidate_token, employer_token, auth_header):
    client.post(
        '/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    client.post(
        '/applications',
        json={'job_id': 1, 'cover_letter': 'I am interested in this position.'},
        headers=auth_header(candidate_token)
    )
    response = client.get('/applications', headers=auth_header(candidate_token))
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_invalid_application_id(client, candidate_token, auth_header):
    response = client.get('/applications/999', headers=auth_header(candidate_token))
    assert response.status_code == 404
    assert 'not found' in response.json['message']

def test_get_application_status(client, candidate_token, employer_token, auth_header):
    client.post(
        '/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    client.post(
        '/applications',
        json={'job_id': 1, 'cover_letter': 'I am interested in this position.'},
        headers=auth_header(candidate_token)
    )
    response = client.get('/applications/1/status', headers=auth_header(candidate_token))
    assert response.status_code == 200
    assert 'status' in response.json

# more tests application
def test_create_application_as_employer_forbidden(client, employer_token, auth_header):
    response = client.post('/applications',
        json={'job_id': 1, 'cover_letter': 'I would love this job'},
        headers=auth_header(employer_token)
    )
    assert response.status_code == 403


def test_create_application_no_token(client):
    response = client.post('/applications',
        json={'job_id': 1, 'cover_letter': 'I would love this job'}
    )
    assert response.status_code == 401


def test_get_applications_no_token(client):
    response = client.get('/applications')
    assert response.status_code == 401

# tests/test_application.py

def test_cannot_view_other_candidates_application(client, candidate_token, employer_token, auth_header):
    # Candidate A creates an application
    job_response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    job_id = job_response.json['id']

    app_response = client.post('/applications',
        json={'job_id': job_id, 'cover_letter': 'From candidate A'},
        headers=auth_header(candidate_token)
    )
    application_id = app_response.json['id']

    # Candidate B registers separately
    client.post('/auth/register', json={
        'email': 'candidate_b@test.com',
        'name': 'Candidate B',
        'password': 'password123',
        'role': 'candidate',
    })
    login_b = client.post('/auth/login', json={
        'email': 'candidate_b@test.com',
        'password': 'password123',
    })
    candidate_b_token = login_b.json['access_token']

    # Candidate B tries to view candidate A's application
    response = client.get(f'/applications/{application_id}', headers=auth_header(candidate_b_token))
    assert response.status_code == 403


def test_cannot_view_other_candidates_application_status(client, candidate_token, employer_token, auth_header):
    job_response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    job_id = job_response.json['id']

    app_response = client.post('/applications',
        json={'job_id': job_id, 'cover_letter': 'From candidate A'},
        headers=auth_header(candidate_token)
    )
    application_id = app_response.json['id']

    client.post('/auth/register', json={
        'email': 'candidate_c@test.com',
        'name': 'Candidate C',
        'password': 'password123',
        'role': 'candidate',
    })
    login_c = client.post('/auth/login', json={
        'email': 'candidate_c@test.com',
        'password': 'password123',
    })
    candidate_c_token = login_c.json['access_token']

    response = client.get(f'/applications/{application_id}/status', headers=auth_header(candidate_c_token))
    assert response.status_code == 403

# tests/test_application.py

def test_create_application_nonexistent_job(client, candidate_token, auth_header):
    response = client.post('/applications',
        json={'job_id': 999999, 'cover_letter': 'Applying to a job that does not exist'},
        headers=auth_header(candidate_token)
    )
    assert response.status_code == 404


def test_create_application_missing_cover_letter(client, candidate_token, employer_token, auth_header):
    job_response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    job_id = job_response.json['id']

    response = client.post('/applications',
        json={'job_id': job_id},  # no cover_letter
        headers=auth_header(candidate_token)
    )
    assert response.status_code == 422

# rate limiting tests for applications
def test_rate_limit_on_applications(mocker):
    # Build a separate app instance with rate limiting enabled
    app = create_app('config.TestingConfigWithRateLimit')

    with app.app_context():
        _db.create_all()
        mocker.patch('jobboard.apis.application.chain')
        client = app.test_client()


        # register + login an employer to create a job
        client.post('/auth/register', json={
            'email': 'rl_employer@test.com', 'name': 'RL Employer',
            'password': 'password123', 'role': 'employer',
        })
        employer_login = client.post('/auth/login', json={
            'email': 'rl_employer@test.com', 'password': 'password123',
        })
        employer_token = employer_login.json['access_token']

        job_response = client.post('/jobs',
            json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
            headers={'Authorization': f'Bearer {employer_token}'}
        )
        job_id = job_response.json['id']

        # register + login a candidate to submit applications
        client.post('/auth/register', json={
            'email': 'rl_candidate@test.com', 'name': 'RL Candidate',
            'password': 'password123', 'role': 'candidate',
        })
        candidate_login = client.post('/auth/login', json={
            'email': 'rl_candidate@test.com', 'password': 'password123',
        })
        candidate_token = candidate_login.json['access_token']
        headers = {'Authorization': f'Bearer {candidate_token}'}

        # fire 10 allowed requests
        for _ in range(10):
            response = client.post('/applications',
                json={'job_id': job_id, 'cover_letter': 'Applying'},
                headers=headers
            )
            assert response.status_code == 201

        # 11th should be rate-limited
        response = client.post('/applications',
            json={'job_id': job_id, 'cover_letter': 'One too many'},
            headers=headers
        )
        assert response.status_code == 429

        _db.session.remove()
        _db.drop_all()