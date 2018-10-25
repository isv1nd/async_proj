import abc


class AbstractUserStorageService(metaclass=abc.ABCMeta):
    def __init__(self, db_engine=None):
        self._db_engine = db_engine

    @abc.abstractmethod
    async def create_user(self, data: dict) -> dict:
        pass

    @abc.abstractmethod
    async def get_users(self) -> list:
        pass

    @abc.abstractmethod
    async def get_user_by_id(self, user_id: int) -> dict:
        pass

    @abc.abstractmethod
    async def delete_user_by_id(self, user_id: int) -> None:
        pass

