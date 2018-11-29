import typing

import pytest
from hamcrest import *
from hamcrest.core.matcher import Matcher
from .data_generators import *
from .base import Client


class BaseResource:
    base_url = ""  # type: str
    data_generator = None  # type: typing.Union[factory.Factory, None]

    def __init__(self, client):
        self.client = client

    async def create(
            self, data: dict=None, expected_status_code: int=201
    ) -> dict:
        data = data or {}

        created_data = self.data_generator.create() \
            if self.data_generator else {}
        created_data.update(**data)

        status_code, response_data, headers = \
            await self.client.post(self.base_url, data=created_data)

        assert_that(status_code, equal_to(expected_status_code))

        if status_code == 201:
            matcher = self.get_matcher(created_data)
            assert_that(response_data, matcher)
        return response_data

    def get_matcher(self, expected_data: dict) -> Matcher:
        matchers = {key: equal_to(value)
                    for key, value
                    in expected_data.items()}
        matchers.update(id=is_(int))
        return has_entries(**matchers)

    async def get_by_id(self, id_: int, expected_status_code: int=200) -> dict:
        status_code, data, _ = await self.client.get(f"{self.base_url}/{id_}")
        assert expected_status_code == status_code
        return data

    async def get_list(self, expected_status_code: int=200) -> dict:
        status_code, data, headers = await self.client.get(self.base_url)
        assert expected_status_code == status_code
        return data

    async def delete(self, id_: int, expected_status_code: int=204) -> None:
        status_code, _, _ = await self.client.delete(f"{self.base_url}/{id_}")
        assert expected_status_code == status_code


class UsersResource(BaseResource):
    base_url = "/users"
    data_generator = UsersFactory

    def get_matcher(self, expected_data: dict) -> Matcher:
        expected_data.pop("password")
        return super().get_matcher(expected_data)


class API:
    def __init__(self, client: Client):
        self.client = client
        self.users = UsersResource(self.client)

    async def clean_resource_instances(self, resources_list: list) -> None:
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
