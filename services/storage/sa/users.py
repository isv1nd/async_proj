from passlib.hash import sha256_crypt

from services.storage import base_exceptions
from services.storage import abstract
from psycopg2 import IntegrityError
from db import tables


class UserStorageService(abstract.AbstractUserStorageService):
    async def create_user(self, data: dict) -> dict:
        data.update(pwd_hash=self._make_password_hash(data.pop("password")))

        async with self._db_engine.acquire() as conn:
            async with conn.begin() as transaction:
                try:
                    result = await conn.execute(tables.users.insert().values(data))
                    id_ = next(iter(result))[0]
                    return_data = \
                        await conn.execute(tables.users.select().where(tables.users.c.id == id_))
                    transaction.commit()
                except Exception as exc:
                    transaction.rollback()
                    if isinstance(exc, IntegrityError) and \
                            "unique" in str(exc).lower():
                        raise base_exceptions.ObjectDuplication
                    raise
            return next(iter(return_data))

    async def get_users(self) -> list:
        async with self._db_engine.acquire() as conn:
            result = await conn.execute(tables.users.select())
            return list(result)

    async def get_user_by_id(self, user_id: int) -> dict:
        async with self._db_engine.acquire() as conn:
            result = await conn.execute(tables.users.select().where(tables.users.c.id == user_id))
            if not result.rowcount:
                raise base_exceptions.ObjectNotFoundException
            return next(iter(result))

    async def delete_user_by_id(self, user_id: int) -> None:
        async with self._db_engine.acquire() as conn:
            result = await conn.execute(tables.users.select().where(tables.users.c.id == user_id))
            if not result.rowcount:
                raise base_exceptions.ObjectNotFoundException
            await conn.execute(tables.users.delete().where(tables.users.c.id == user_id))

    @staticmethod
    def _make_password_hash(raw_password: str) -> str:
        return sha256_crypt.hash(raw_password)
