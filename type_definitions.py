from datetime import datetime
from pprint import pformat


class User:
    name: str
    email: str
    password: str
    id: str

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        fields = {field: getattr(self, field) for field in self._fields}
        return f"{self.__class__.__name__}({pformat(fields)})"

    def to_dict(self):
        return self.__dict__


class ChatCompletion:
    content: str
    created_at: datetime
    model: str
    id: str

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        fields = {field: getattr(self, field) for field in self._fields}
        return f"{self.__class__.__name__}({pformat(fields)})"

    def to_dict(self):
        return self.__dict__
