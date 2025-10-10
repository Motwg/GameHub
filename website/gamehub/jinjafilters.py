from typing import Literal, LiteralString

from inflection import parameterize
from markupsafe import Markup


def slugify(variable: str) -> str:
    return parameterize(variable)[:80].rstrip('-')


# This data would better go in a database...
error_dict = {
    'Err1': 'ERROR 1: watch out for error n.1!',
    'Err2': 'ERROR 2: watch out for error n.2!',
    'Err9': 'ERROR 9: watch out for error n.9!',
}


def display_error(err_num: Literal[1, 2, 9]) -> str:
    key = 'Err' + str(err_num)
    return error_dict[key]


msg_dict = {
    'miss_username': '<p>Please enter your username</p>',
    'miss_room': '<p>Please join a room</p>',
}


def display_message(msg_key: LiteralString) -> Markup:
    # THE DECORATOR IS NEEDED TO DISABLE CACHING OF JINJA CALLS!!!
    return Markup('{}').format(msg_dict.get(msg_key, 'Something gone wrong'))
