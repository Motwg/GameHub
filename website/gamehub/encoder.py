from typing import Any, override

from flask.json.provider import DefaultJSONProvider


class CustomJSONProvider(DefaultJSONProvider):
    @override
    def dumps(self, obj: Any, **kwargs: Any) -> str:
        return super().dumps(obj, **kwargs)
