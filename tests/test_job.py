def test_create_job_as_employer(client, employer_token, auth_header):
    response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    assert response.status_code == 201


def test_view_jobs(client, employer_token, auth_header):
    client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote', 'tags': 'Python, Flask'},
        headers=auth_header(employer_token)
    )
    client.post('/jobs',
        json={'title': 'Frontend Dev', 'description': 'Build UI', 'location': 'Remote', 'tags': 'JavaScript, React'},
        headers=auth_header(employer_token)
    )
    response = client.get('/jobs')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_view_job_details(client, employer_token, auth_header):
    client.post(
        '/jobs', 
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote', 'tags': 'Python, Flask'},
        headers=auth_header(employer_token)
    )
    response = client.get('/jobs/1')
    assert response.status_code == 200
    assert response.json['title'] == 'Backend Dev'

def test_invalid_job_id(client):
    response = client.get('/jobs/999')
    assert response.status_code == 404
    assert 'not found' in response.json['message']


def test_update_job_as_employer(client, employer_token, auth_header):
    client.post(
        '/jobs', 
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote', 'tags': 'Python, Flask'},
        headers=auth_header(employer_token)
    )
    response = client.put(
        '/jobs/1',
        json={'title': 'Senior Backend Dev'},
        headers=auth_header(employer_token)
    )
    assert response.status_code == 200
    assert response.json['title'] == 'Senior Backend Dev'


def test_delete_job_as_employer(client, employer_token, auth_header):
    client.post(
        '/jobs', 
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote', 'tags': 'Python, Flask'},
        headers=auth_header(employer_token)
    )
    response = client.delete('/jobs/1', headers=auth_header(employer_token))
    assert response.status_code == 204

# more tests 
def test_create_job_as_candidate_forbidden(client, candidate_token, auth_header):
    response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(candidate_token)
    )
    assert response.status_code == 403


def test_create_job_no_token(client):
    response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'}
    )
    assert response.status_code == 401


def test_update_job_as_candidate_forbidden(client, employer_token, candidate_token, auth_header):
    create_response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    job_id = create_response.json['id']

    response = client.put(f'/jobs/{job_id}',
        json={'title': 'Hacked Title'},
        headers=auth_header(candidate_token)
    )
    assert response.status_code == 403


def test_delete_job_as_candidate_forbidden(client, employer_token, candidate_token, auth_header):
    create_response = client.post('/jobs',
        json={'title': 'Backend Dev', 'description': 'Build stuff', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    job_id = create_response.json['id']

    response = client.delete(f'/jobs/{job_id}', headers=auth_header(candidate_token))
    assert response.status_code == 403

# tests/test_job.py

def test_create_job_missing_title(client, employer_token, auth_header):
    response = client.post('/jobs',
        json={'description': 'Build stuff', 'location': 'Remote'},  # no title
        headers=auth_header(employer_token)
    )
    assert response.status_code == 422


def test_filter_jobs_by_title(client, employer_token, auth_header):
    client.post('/jobs',
        json={'title': 'Backend Engineer', 'description': 'Build APIs', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )
    client.post('/jobs',
        json={'title': 'Frontend Engineer', 'description': 'Build UI', 'location': 'Remote'},
        headers=auth_header(employer_token)
    )

    response = client.get('/jobs?title=backend')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == 'Backend Engineer'


def test_pagination_returns_header(client, employer_token, auth_header):
    for i in range(3):
        client.post('/jobs',
            json={'title': f'Job {i}', 'description': 'Desc', 'location': 'Remote'},
            headers=auth_header(employer_token)
        )

    response = client.get('/jobs?page=1&page_size=2')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert 'X-Pagination' in response.headers