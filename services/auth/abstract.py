import abc
import typing
from aiohttp.web import web_request
from services.auth import model
from services.storage import abstract


class AbstractAuthenticationService(metaclass=abc.ABCMeta):
    def __init__(self, request: web_request.Request):
        self._request = request
        self._user_storage_service = self.get_user_storage_service()

    @abc.abstractmethod
    def get_user_storage_service(self) -> abstract.AbstractUserStorageService:
        pass

    @abc.abstractmethod
    async def get_authenticated_user(self) -> typing.Union[None, model.BaseUser]:
        pass

    @abc.abstractmethod
    async def authenticate(self, email: str, password: str) -> str:
        pass
