from fastapi.testclient import TestClient
import pytest


def get_self(token: str, client: TestClient) -> None:
    response = client.get('/users/@me', headers={'Authorization': token})

    assert response.status_code == 200
    data = response.json()
    # TODO: don't let flags be more than all current combined

    # the id should be stringified
    assert isinstance(data['id'], str)
    # discriminator shall only be a string
    assert isinstance(data['discriminator'], str)
    # flags may only be integers
    assert isinstance(data['flags'], int)
    # discriminator can only be 4 characters long
    assert len(data['discriminator']) == 4

    assert data['username'] == 'test'
    assert data['email'] == 'test@testing.io'
    assert data['system'] == False
    assert data['suspended'] == False

    with pytest.raises(KeyError):
        data['password']

    with pytest.raises(KeyError):
        data['deletor_job_id']
