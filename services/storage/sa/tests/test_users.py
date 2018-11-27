import pytest
import copy
import asynctest
import factory
from hamcrest import *
from sqlalchemy.sql import dml

from services.storage.sa import users


class UsersFactory(factory.DictFactory):
    name = factory.Faker('name')
    birthday = factory.Faker('date')


@pytest.mark.usefixtures('user_setup')
class TestUsers:
    @pytest.fixture
    def user_setup(self):
        self.db_engine = asynctest.MagicMock()
        self.service = users.UserStorageService(db_engine=self.db_engine)
        self.input_data = UsersFactory.create()
        self.id_ = 1

    async def test_create_user(self):
        execute_mock = \
            self.db_engine.acquire.return_value.__aenter__.return_value.execute = \
            asynctest.CoroutineMock(return_value=[(self.id_,)])

        result = await self.service.create_user(copy.copy(self.input_data))

        self.input_data.update(id=self.id_)
        assert_that(result, equal_to(self.input_data))
        self.db_engine.acquire.assert_called_once()
        assert_that(execute_mock, has_properties(
            await_count=equal_to(1),
            call_args=has_item(
                has_item(
                    instance_of(dml.Insert)
                )
            )
        ))
