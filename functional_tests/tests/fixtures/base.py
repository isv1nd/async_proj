import os
from urllib import parse

import aiohttp
from pytest import *


class Client:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._base_url = os.environ.get("API_URL", "http://localhost:9001")

    def _build_full_url(self, url: str) -> str:
        return parse.urljoin(self._base_url, url)

    async def get(self, url: str, *args, **kwargs):
        async with self._session.get(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    async def post(self, url: str,  *args, **kwargs):
        async with self._session.post(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    async def put(self, url: str, *args, **kwargs):
        async with self._session.put(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    async def patch(self, url: str, *args, **kwargs):
        async with self._session.patch(
            self._build_full_url(url), *args, **kwargs
        ) as response:
            return response.status, await response.json(), response.headers

    async def delete(self, url: str, **kwargs):
        async with self._session.delete(
            self._build_full_url(url), **kwargs
        ) as response:
            return response.status, response.headers


@fixture
async def client_session(loop):
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@fixture
async def client(loop, client_session):
    return Client(client_session)
