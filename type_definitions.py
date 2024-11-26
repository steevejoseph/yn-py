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
        # Use pformat to pretty-print the dictionary of attributes
        attrs = vars(self)
        # Convert the attributes to a pretty string format
        pretty_str = f"User({self.__class__.__name__}):\n{pformat(attrs, indent=2)}"
        return pretty_str

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
        # Use pformat to pretty-print the dictionary of attributes
        attrs = vars(self)
        # Convert the attributes to a pretty string format
        pretty_str = f"User({self.__class__.__name__}):\n{pformat(attrs, indent=2)}"
        return pretty_str

    def to_dict(self):
        return self.__dict__
