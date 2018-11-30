import pytest
from hamcrest import *


@pytest.fixture
async def authenticate_request(api):
    # FIXME: it should me made more convenient
    await api.authenticate_request()
    yield


@pytest.mark.usefixtures('clean_up_users', 'authenticate_request')
class TestUsers:
    async def test_users_list(self, api):
        created_data = await api.users.post()
        list_data = await api.users.get_list()

        assert_that(list_data, has_items(created_data))

    async def test_create_user(self, api):
        await api.users.post()

    async def test_create_user_return_422_if_data_is_invalid(self, api):
        await api.users.post(data=dict(email='Invalid'),
                             expected_status_code=422)

    async def test_create_user_return_409_if_data_duplicated(self, api):
        first_user_data = await api.users.post()
        await api.users.post(data=dict(email=first_user_data['email']),
                             expected_status_code=409)

    async def test_get_user_by_id(self, api):
        created_data = await api.users.post()
        get_data = await api.users.get_by_id(created_data["id"])

        assert_that(get_data, equal_to(created_data))

    async def test_delete_user(self, api):
        created_data = await api.users.post()
        await api.users.delete(created_data["id"])
        await api.users.get_by_id(created_data["id"], expected_status_code=404)
