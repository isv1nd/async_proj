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
    password = "password"
    is_active = False


@pytest.mark.usefixtures('user_setup')
class TestUsers:
    @pytest.fixture
    def user_setup(self):
        self.db_engine = asynctest.MagicMock()
        self.service = users.UserStorageService(db_engine=self.db_engine)
        self.input_data = UsersFactory.create()

    @asynctest.patch.object(dml.Insert, 'values')
    async def test_create_user(self, insert_values_mock):
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
        self._check_sa_insert_mock(insert_values_mock)
        self._check_sa_execute_mocks(execute_mock, insert_values_mock)

    @staticmethod
    def _check_sa_execute_mocks(execute_mock, insert_values_mock):
        assert_that(execute_mock, has_properties(
            await_count=equal_to(2),
            call_args_list=has_items(
                has_item(
                    has_item(
                        is_(insert_values_mock.return_value)
                    )
                ),
                has_item(
                    has_item(
                        instance_of(selectable.Select)
                    )
                ),
            )
        ))

    def _check_sa_insert_mock(self, insert_values_mock):
        assert_that(insert_values_mock, has_properties(
            call_count=1,
            call_args=has_item(
                has_item(
                    has_entries(
                        full_name=equal_to(self.input_data["full_name"]),
                        email=equal_to(self.input_data["email"]),
                        pwd_hash=instance_of(str)
                    )
                )
            )
        ))
