from mongoengine import *
from pprint import pformat

from type_definitions import ChatCompletion, User


class BaseDocument(Document):
    meta = {"abstract": True}

    def __str__(self):
        fields = {field: getattr(self, field) for field in self._fields}
        return f"{self.__class__.__name__}({pformat(fields)})"
