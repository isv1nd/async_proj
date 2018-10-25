import logging

from aiohttp import web

from services.storage import base_exceptions

LOG = logging.getLogger("aiohttp.server")


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if 200 <= response.status < 400:
            return response
        message = response.message
        status = response.status
    except web.HTTPException as ex:
        if 200 <= ex.status < 400:
            raise
        message = ex.reason
        status = ex.status

    except base_exceptions.ObjectNotFoundException:
        message = "Object not found"
        status = 404
    except Exception as exc:
        LOG.exception(exc)
        message = "Server error occurred"
        status = 500

    return web.json_response({"error": message, "status": status}, status=status)
