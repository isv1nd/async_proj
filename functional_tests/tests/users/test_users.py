import pytest


class TestUsers(object):
    @pytest.fixture(autouse=True)
    async def clean_up(self, client):
        yield
        for log_item in filter(
            lambda obj:
                obj["request"]["method"] == "post"
                and obj["request"]['args'][0] == '/users'
                and obj['response']['status'] == 201,
            client.log_request
        ):
            id_ = log_item['response']['data']['id']
            if any(
                    filter(
                        lambda obj:
                            obj["request"]["method"] == "delete"
                            and obj["request"]['args'][0] == f'/users/{id_}'
                            and obj['response']['status'] == 204,
                        client.log_request
                    )
            ):
                continue
            status, _, _ = await client.delete(f'/users/{id_}')
            assert status == 204

    async def test_users_list(self, client):
        create_data = {
            "name": "Andrey",
            "birthday": "1988-01-12"
        }
        status, created_data, _ = await client.post('/users', data=create_data)

        assert status == 201

        status, data, _ = await client.get('/users')

        assert status == 200
        assert next(
            filter(lambda item: item["id"] == created_data["id"], data)
        ) == created_data

    async def test_create_user(self, client):
        create_data = {
            "name": "Andrey",
            "birthday": "1988-01-12"
        }
        status, created_data, _ = await client.post('/users', data=create_data)

        assert status == 201
        assert "id" in created_data
        assert created_data["name"] == create_data["name"]
        assert created_data["birthday"] == create_data["birthday"]

    async def test_get_user_by_id(self, client):
        create_data = {
            "name": "Andrey",
            "birthday": "1988-01-12"
        }
        status, created_data, _ = await client.post('/users', data=create_data)

        assert status == 201
        assert "id" in created_data

        status, get_data, _ = await client.get(f'/users/{created_data["id"]}')

        assert get_data["name"] == create_data["name"]
        assert get_data["birthday"] == create_data["birthday"]

    async def test_delete_user(self, client):
        create_data = {
            "name": "Andrey",
            "birthday": "1988-01-12"
        }
        status, created_data, _ = await client.post('/users', data=create_data)

        assert status == 201
        assert "id" in created_data

        status, _, _ = await client.delete(f'/users/{created_data["id"]}')

        assert status == 204

        get_status, _, _ = await client.get(f'/users/{created_data["id"]}')
        assert get_status == 404
