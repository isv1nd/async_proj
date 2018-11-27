import pytest
from hamcrest import *


@pytest.fixture
async def clean_up_users(api):
    yield
    resources_list = ['users']
    await api.clean_resource_instances(resources_list)


@pytest.mark.usefixtures('clean_up_users')
class TestUsers:
    async def test_users_list(self, client, api):
        created_data = await api.users.create()
        list_data = await api.users.get_list()

        assert_that(list_data, has_items(created_data))

    async def test_create_user(self, api):
        await api.users.create()

    async def test_create_user_return_422_if_data_is_invalid(self, api):
        await api.users.create(data=dict(birthday='Invalid date'),
                               expected_status_code=422)

    async def test_get_user_by_id(self, api):
        created_data = await api.users.create()
        get_data = await api.users.get_by_id(created_data["id"])

        assert_that(get_data, equal_to(created_data))

    async def test_delete_user(self, api):
        created_data = await api.users.create()
        await api.users.delete(created_data["id"])
        await api.users.get_by_id(created_data["id"], expected_status_code=404)
