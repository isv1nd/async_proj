class TestUsers(object):
    async def test_users_list(self, client):
        status, data, _ = await client.get('/users')

        assert status == 200
        assert data == []
