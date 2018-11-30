from aiohttp import web
from aiohttp import web_exceptions

from api.v1.permissions import abstract


class IsAuthenticated(abstract.AbstractPermission):
    raise_exception = web_exceptions.HTTPUnauthorized

    @classmethod
    def has_permission(cls, request: web.Request) -> bool:
        # return bool(getattr(request, 'user', None))
        return bool(request.user)
