import pytest


@pytest.mark.usefixtures('clean_up_users')
class TestAuth:
    async def test_get_token(self, api):
        await api.authenticate_request()
