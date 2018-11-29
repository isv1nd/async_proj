

class BaseUser:
    def __init__(self, data: dict):
        self._data = data

    @property
    def full_name(self) -> str:
        return self._data.get("full_name", "")

    @property
    def email(self) -> str:
        return self._data["email"]

    @property
    def is_active(self) -> bool:
        return self._data["is_active"]

    def __str__(self):
        return self.email


class User(BaseUser):
    pass
