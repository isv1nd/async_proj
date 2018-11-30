import logging

from aiohttp import web

from services.storage import base_exceptions
from services.auth import exceptions as auth_exceptions
import utils
import settings

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
    except base_exceptions.ObjectDuplication:
        message = "Object duplication"
        status = 409
    except auth_exceptions.BaseAuthenticationException as exc:
        message = str(exc) or "You are not logged-in"
        status = 401
    except Exception as exc:
        LOG.exception(exc)
        message = "Server error occurred"
        status = 500

    return web.json_response({"error": message, "status": status}, status=status)


@web.middleware
async def auth_middleware(request, handler):
    auth_service = utils.import_from_str(settings.AUTHENTICATION_CLASS)(request)
    request.user = await auth_service.get_authenticated_user()
    response = await handler(request)
    return response
