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
        self.token = None

    def set_token(self, token):
        self.token = token

    async def post(
            self, data: dict=None, expected_status_code: int=201,
            success_status_code: int=201
    ) -> dict:
        data = data or {}

        created_data = self.data_generator.create() \
            if self.data_generator else {}
        created_data.update(**data)

        status_code, response_data, headers = \
            await self.client.post(self.base_url, data=created_data,
                                   headers=self._get_headers())

        assert_that(status_code, equal_to(expected_status_code))

        if status_code == success_status_code:
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
        status_code, data, _ = await self.client.get(f"{self.base_url}/{id_}",
                                                     headers=self._get_headers())
        assert expected_status_code == status_code
        return data

    async def get_list(self, expected_status_code: int=200) -> dict:
        status_code, data, headers = await self.client.get(self.base_url,
                                                           headers=self._get_headers())
        assert expected_status_code == status_code
        return data

    async def delete(self, id_: int, expected_status_code: int=204) -> None:
        status_code, _, _ = await self.client.delete(f"{self.base_url}/{id_}",
                                                     headers=self._get_headers())
        assert expected_status_code == status_code

    def _get_headers(self):
        headers = {}
        if self.token:
            headers.update(Authorization=f"Auth {self.token}")
        return headers


class UsersResource(BaseResource):
    base_url = "/users"
    data_generator = UsersFactory

    def get_matcher(self, expected_data: dict) -> Matcher:
        expected_data.pop("password")
        return super().get_matcher(expected_data)


class AuthenticateResource(BaseResource):
    base_url = "/auth/authenticate"

    def get_matcher(self, expected_data: dict) -> Matcher:
        return has_entries(token=is_(str))


class API:
    def __init__(self, client: Client):
        self.client = client
        self.user = None
        self.token = None

        # Resource list
        self.users = UsersResource(self.client)
        self.authenticate = AuthenticateResource(self.client)

    async def authenticate_request(self, email: str or None=None, password: str or None=None):
        if not (email and password):
            user_data = self.users.data_generator.create()
            email, password = user_data["email"], user_data["password"]

            admin_response = await self.authenticate.post(
                {"email": "admin@admin.ru", "password": "admin"},
                expected_status_code=200, success_status_code=200
            )
            self.users.token = admin_response["token"]
            self.user = await self.users.post(user_data)

        result = await self.authenticate.post(
            {"email": email, "password": password},
            expected_status_code=200, success_status_code=200
        )
        self.token = result["token"]

        for attr in self.__dir__():
            if isinstance(attr, BaseResource):
                attr.set_token(self.token)

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
