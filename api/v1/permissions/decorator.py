import typing

from aiohttp import web_exceptions

from api.v1.permissions import abstract


def check_permissions(permission_classes: typing.List[abstract.AbstractPermission]):
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            for class_ in permission_classes:
                if not class_.has_permission(self.request):
                    raise class_.raise_exception or web_exceptions.HTTPForbidden
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator
