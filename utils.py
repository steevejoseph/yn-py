import json
from flask import Response, jsonify

from datetime import datetime


class MyClassJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, object):
            return obj.to_dict()  # Serialize MyClass instances using to_dict
        return super().default(obj)  # Let the default encoder handle other types


def create_response(message: str, status_code: int, data=None, reason=None) -> Response:
    res = jsonify({"message": message, "data": data, "reason": reason})
    res.status_code = status_code
    return res
