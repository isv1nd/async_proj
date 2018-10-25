from aiohttp import web


class RootView(web.View):
    async def get(self):
        return web.json_response({"message": "Hello, user!"}, status=200)
