import abc

from aiohttp import web
from webargs.aiohttpparser import use_args
from api.v1.schemes import auth as auth_schemes
from services.auth import jwt
from services.auth import abstract


class AbstractAuthView(web.View, metaclass=abc.ABCMeta):
    def __init__(self, request):
        super().__init__(request)
        self.auth_service = self._construct_auth_service()

    @abc.abstractmethod
    def _construct_auth_service(self) -> abstract.AbstractAuthenticationService:
        pass


class JWTAuthView(AbstractAuthView):
    @use_args(auth_schemes.AuthenticationSchema())
    async def post(self, data):
        token = await self.auth_service.authenticate(**data)

        return web.json_response(
            auth_schemes.TokenResponseScheme().dump({"token": token}).data,
            status=200
        )

    def _construct_auth_service(self):
        return jwt.JWTTokenAuthenticationService(request=self.request)
