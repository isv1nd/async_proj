import os
from urllib import parse

import aiohttp
from pytest import *


def request_log(func):
    async def wrapper(self, *args, **kwargs):
        status, data, headers = await func(self, *args, **kwargs)
        self.log_request.append({
            "request": {
                "method": func.__name__,
                "args": args,
                "kwargs": kwargs
            },
            "response": {
                "status": status,
                "data": data,
                "headers": headers
            }
        })
        return status, data, headers
    return wrapper


class Client:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._base_url = os.environ.get("API_URL", "http://localhost:9001")
        self.log_request = []

    def _build_full_url(self, url: str) -> str:
        return parse.urljoin(self._base_url, url)

    @request_log
    async def get(self, url: str, *args, **kwargs):
        async with self._session.get(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    @request_log
    async def post(self, url: str,  *args, **kwargs):
        async with self._session.post(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    @request_log
    async def put(self, url: str, *args, **kwargs):
        async with self._session.put(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    @request_log
    async def patch(self, url: str, *args, **kwargs):
        async with self._session.patch(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    @request_log
    async def delete(self, url: str, **kwargs):
        async with self._session.delete(
            self._build_full_url(url), **kwargs
        ) as response:
            return response.status, None, response.headers


@fixture
async def client_session(loop):
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@fixture
async def client(loop, client_session):
    return Client(client_session)


@fixture
async def clean_up_users(api):
    yield
    resources_list = ['users']
    await api.clean_resource_instances(resources_list)
