import pytest
import copy
import asynctest
import factory
from hamcrest import *
from sqlalchemy.sql import dml
from sqlalchemy.sql import selectable

from services.storage.sa import users


class UsersFactory(factory.DictFactory):
    full_name = factory.Faker('name')
    email = factory.Faker('email')
    is_active = False


@pytest.mark.usefixtures('user_setup')
class TestUsers:
    @pytest.fixture
    def user_setup(self):
        self.db_engine = asynctest.MagicMock()
        self.service = users.UserStorageService(db_engine=self.db_engine)
        self.input_data = UsersFactory.create()

    async def test_create_user(self):
        response_data = copy.copy(self.input_data)
        execute_mock = \
            self.db_engine.acquire.return_value.__aenter__.return_value.execute = \
            asynctest.CoroutineMock(
                side_effect=(
                    [(1,)],
                    [response_data]
                )
            )

        result = await self.service.create_user(copy.copy(self.input_data))

        assert_that(result, equal_to(response_data))
        self.db_engine.acquire.assert_called_once()
        assert_that(execute_mock, has_properties(
            await_count=equal_to(2),
            call_args_list=has_items(
                has_item(
                    has_item(
                        instance_of(dml.Insert)
                    )
                ),
                has_item(
                    has_item(
                        instance_of(selectable.Select)
                    )
                ),
            )
        ))
