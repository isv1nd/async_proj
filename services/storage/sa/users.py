from services.storage import base_exceptions
from services.storage import abstract
from db import tables


class UserStorageService(abstract.AbstractUserStorageService):
    async def create_user(self, data: dict) -> dict:
        async with self._db_engine.acquire() as conn:
            result = await conn.execute(tables.users.insert().values(data))
            data.update(id=next(iter(result))[0])
            return data

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
