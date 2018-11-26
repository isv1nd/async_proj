import typing

import pytest
from hamcrest import *
from .data_generators import *


class BaseResource:
    base_url = ""  # type: str
    data_generator = None  # type: typing.Union[factory.Factory, None]

    def __init__(self, client):
        self.client = client

    async def create(
            self, data=None, expected_status_code=201
    ):
        data = data or {}

        created_data = self.data_generator.create() \
            if self.data_generator else {}
        created_data.update(**data)

        status_code, response_data, headers = \
            await self.client.post(self.base_url, data=created_data)

        assert expected_status_code == status_code

        if status_code == 201:
            matcher = {key: equal_to(value)
                       for key, value
                       in created_data.items()}
            matcher.update(id=is_(int))
            assert_that(response_data, has_entries(**matcher))
        return response_data

    async def get_by_id(self, id_, expected_status_code=200):
        status_code, data, _ = await self.client.get(f"{self.base_url}/{id_}")
        assert expected_status_code == status_code
        return data

    async def get_list(self, expected_status_code=200):
        status_code, data, headers = await self.client.get(self.base_url)
        assert expected_status_code == status_code
        return data

    async def delete(self, id_, expected_status_code=204):
        status_code, _, _ = await self.client.delete(f"{self.base_url}/{id_}")
        assert expected_status_code == status_code


class UsersResource(BaseResource):
    base_url = "/users"
    data_generator = UsersFactory


class API:
    def __init__(self, client):
        self.client = client
        self.users = UsersResource(self.client)

    async def clean_resource_instances(self, resources_list):
        for resource_name in resources_list:
            resource = getattr(self, resource_name)
            for log_item in filter(
                    lambda obj:
                    obj["request"]["method"] == "post"
                    and obj["request"]['args'][0] == resource.base_url
                    and obj['response']['status'] == 201,
                    self.client.log_request
            ):
                id_ = log_item['response']['data']['id']
                if any(
                        filter(
                            lambda obj:
                            obj["request"]["method"] == "delete"
                            and obj["request"]['args'][
                                0] == f'{resource.base_url}/{id_}'
                            and obj['response']['status'] == 204,
                            self.client.log_request
                        )
                ):
                    continue
                await resource.delete(id_)


@pytest.fixture
def api(client):
    return API(client)

