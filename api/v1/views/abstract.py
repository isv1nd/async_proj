import abc

from aiohttp import web
from services.storage import abstract


class AbstractUserView(web.View, metaclass=abc.ABCMeta):
    def __init__(self, request):
        super().__init__(request)
        self.user_storage_service = self._construct_db_service()

    @abc.abstractmethod
    def _construct_db_service(self) -> abstract.AbstractUserStorageService:
        pass
