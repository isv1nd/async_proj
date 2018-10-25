class BaseDBExceptions(Exception):
    pass


class ObjectNotFoundException(BaseDBExceptions):
    pass


class MultipleObjectsReturnedException(BaseDBExceptions):
    pass
