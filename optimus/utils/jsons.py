import datetime
import json
from pathlib import Path


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Additional opiniated support for more basic object types.

    Usage sample: ::

        json.dumps(..., cls=ExtendedJsonEncoder)
    """
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        # Support for pathlib.Path to a string
        if isinstance(obj, Path):
            return str(obj)
        # Support for set to a list
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
