from aiohttp import web
from webargs.aiohttpparser import use_args
from api.v1.schemes import users
from services.storage.sa import users as users_service
from api.v1.views import abstract


class BaseUserView(abstract.AbstractUserView):
    def _construct_db_service(self):
        return users_service.UserStorageService(db_engine=self.request.app['db'])


class UsersView(BaseUserView):
    @use_args(users.UserSchema())
    async def post(self, data):
        result = await self.user_storage_service.create_user(data)

        return web.json_response(
            users.UserSchema().dump(result).data,
            status=201
        )

    async def get(self):
        result = await self.user_storage_service.get_users()

        return web.json_response(
            users.UserSchema(many=True).dump(result).data,
            status=200
        )


class UsersDetailView(BaseUserView):
    async def get(self):
        id_ = int(self.request.match_info['id'])

        result = await self.user_storage_service.get_user_by_id(id_)

        return web.json_response(
            users.UserSchema().dump(result).data,
            status=200
        )

    async def delete(self):
        id_ = int(self.request.match_info['id'])

        await self.user_storage_service.delete_user_by_id(id_)

        return web.Response(
            status=204
        )
