import abc
from aiohttp import web
from aiohttp import web_exceptions


class AbstractPermission(metaclass=abc.ABCMeta):
    raise_exception = None  # type: web_exceptions.HTTPException

    @classmethod
    @abc.abstractmethod
    def has_permission(cls, request: web.Request) -> bool:
        pass
