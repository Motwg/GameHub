from typing import Any, override

from flask.json.provider import DefaultJSONProvider

from website.gamehub.model.user import User


class CustomJSONProvider(DefaultJSONProvider):
    @override
    def dumps(self, obj: Any, **kwargs: Any) -> str:
        # if isinstance(obj, User):
        #     return {
        #         'username': obj['username'],
        #         'user_id': str(obj['user_id']),
        #         'points': obj['points'],
        #         'is_ready': obj['is_ready'],
        #     }.__str__()
        return super().dumps(obj, **kwargs)
