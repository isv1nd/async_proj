from aiohttp import web
from api import urls
from api import middleware
from aiopg import sa
import settings

MIDDLEWARE_LIST = [
    middleware.error_middleware
]


async def init_pg(app):
    engine = await sa.create_engine(
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        minsize=settings.MINSIZE,
        maxsize=settings.MAXSIZE,
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def init_func(*args, **kwargs):
    app = web.Application(middlewares=MIDDLEWARE_LIST)

    app.add_routes(urls.urls)

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    return app
