from aiohttp import web
from api.v1.views import users
from api.v1.views import auth
from api.v1.views import root


urls = [
    web.view("/", root.RootView),
    web.view("/users", users.UsersView),
    web.view("/users/{id:\d+}", users.UsersDetailView),
    web.view("/auth/authenticate", auth.JWTAuthView),
]
