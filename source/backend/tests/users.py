import pytest


@pytest.mark.incremental
class UserRouter:
    def test_register(client):
        resp = client.post(
            '/v1/register', json={'username': 'test', 'email': 'test@test.com', 'password': 'ABcdef148'}
        )
        assert resp.status == 201
        assert resp.json['username'] == 'test'
        assert resp.json['email'] == 'test'
        with pytest.raises(KeyError):
            resp.json['password']
        assert isinstance(resp.json['id'], str)
        assert isinstance(resp.json['discriminator'], str)
        assert resp.json['system'] is False
        assert resp.json['suspended'] is False
        assert resp.json['token']
        pytest.user_token = resp.json['token']

    def test_get_me(client):
        resp = client.get('/v1/users/@me', headers={'Authorization': pytest.user_token})
        assert resp.status == 200
        assert resp.json['username'] == 'test'
        assert resp.json['email'] == 'test'
        with pytest.raises(KeyError):
            resp.json['password']
        assert isinstance(resp.json['id'], str)
        assert isinstance(resp.json['discriminator'], str)
        assert resp.json['system'] is False
        assert resp.json['suspended'] is False
        with pytest.raises(KeyError):
            assert resp.json['token']
