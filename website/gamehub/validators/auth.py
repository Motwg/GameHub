def validate_username(username):
    if username is not None and all((isinstance(username, str), len(username) > 3)):
        return True
    return False
