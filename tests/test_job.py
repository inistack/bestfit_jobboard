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