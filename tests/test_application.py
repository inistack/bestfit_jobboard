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