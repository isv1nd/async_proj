import typing
import datetime
import time

import jwt
import calendar

from services.storage import abstract as storage_abstract
from services.auth import abstract as auth_abstract
from services.storage.sa import users
from services.storage import base_exceptions as storage_exceptions
from services.auth import model
from services.auth import exceptions as auth_exceptions
import settings


class JWTTokenAuthenticationService(auth_abstract.AbstractAuthenticationService):
    def get_user_storage_service(self) -> storage_abstract.AbstractUserStorageService:
        return users.UserStorageService(db_engine=self._request.app['db'])

    async def get_authenticated_user(self) -> typing.Union[None, model.BaseUser]:
        try:
            token = self._get_token_from_request()
            user = model.User(
                await self._user_storage_service.get_user_by_id(token["user_id"])
            )
            if not user.is_active:
                return None
            return user
        except (auth_exceptions.BaseAuthenticationException,
                storage_exceptions.ObjectNotFoundException):
            return None

    async def authenticate(self, email: str, password: str) -> str:
        try:
            user = await self._user_storage_service.get_user_by_credentials(email, password)
        except storage_exceptions.ObjectNotFoundException:
            raise auth_exceptions.InvalidCredentialsException

        if not user["is_active"]:
            raise auth_exceptions.UserIsInactiveException

        payload = {
            "user_id": user["id"],
            "exp": calendar.timegm(
                datetime.datetime.utcnow().timetuple()
            ) + settings.JWT_TTL_SEC
        }
        return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM).decode()

    def _get_token_from_request(self) -> dict:
        try:
            scheme, token = self._request.headers.get(
                settings.JWT_HEADER_NAME
            ).strip().split(' ')
        except AttributeError:
            raise auth_exceptions.CredentialsWereNotProvidedException

        if scheme != settings.JWT_TOKEN_SCHEME:
            raise auth_exceptions.InvalidTokenException

        try:
            decoded = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=settings.JWT_ALGORITHM,
            )
        except jwt.InvalidTokenError:
            raise auth_exceptions.InvalidTokenException

        return decoded
