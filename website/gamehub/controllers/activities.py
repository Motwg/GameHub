from website.gamehub.db import db
from website.gamehub.model.room import LiteralActivities


def get_activity(activity: LiteralActivities) -> str:
    return db.activities[activity]
