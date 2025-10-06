from typing import Literal
from website.gamehub.db import db


def get_activity(activity: Literal['cah']) -> str:
    return db.activities.get(activity)
