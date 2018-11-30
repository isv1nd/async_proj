import abc

from aiohttp import web
from webargs.aiohttpparser import use_args
from api.v1.schemes import users
from services.storage.sa import users as users_service
from services.storage import abstract
from api.v1.permissions.decorator import check_permissions
from api.v1.permissions import base


class AbstractUserView(web.View, metaclass=abc.ABCMeta):
    def __init__(self, request):
        super().__init__(request)
        self.user_storage_service = self._construct_db_service()

    @abc.abstractmethod
    def _construct_db_service(self) -> abstract.AbstractUserStorageService:
        pass


class BaseUserView(AbstractUserView):
    def _construct_db_service(self):
        return users_service.UserStorageService(db_engine=self.request.app['db'])


class UsersView(BaseUserView):
    @use_args(users.UserSchema())
    @check_permissions([base.IsAuthenticated])
    async def post(self, data):
        result = await self.user_storage_service.create_user(data)

        return web.json_response(
            users.UserSchema().dump(result).data,
            status=201
        )

    @check_permissions([base.IsAuthenticated])
    async def get(self):
        result = await self.user_storage_service.get_users()

        return web.json_response(
            users.UserSchema(many=True).dump(result).data,
            status=200
        )


class UsersDetailView(BaseUserView):
    @check_permissions([base.IsAuthenticated])
    async def get(self):
        id_ = int(self.request.match_info['id'])

        result = await self.user_storage_service.get_user_by_id(id_)

        return web.json_response(
            users.UserSchema().dump(result).data,
            status=200
        )

    @check_permissions([base.IsAuthenticated])
    async def delete(self):
        id_ = int(self.request.match_info['id'])

        await self.user_storage_service.delete_user_by_id(id_)

        return web.Response(
            status=204
        )
