from website.gamehub.db import LiteralActivities, db


def get_activity(activity: LiteralActivities) -> str:
    return db.activities[activity]
