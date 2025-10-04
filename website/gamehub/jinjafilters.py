from inflection import parameterize
from markupsafe import Markup


def slugify(variable):
    return parameterize(variable)[:80].rstrip('-')


# This data would better go in a database...
error_dict = {
    "Err1": "ERROR 1: watch out for error n.1!",
    "Err2": "ERROR 2: watch out for error n.2!",
    "Err9": "ERROR 9: watch out for error n.9!"
}


def display_error(err_num):
    key = "Err" + str(err_num)
    result = error_dict[key]
    return result


msg_dict = {
    'miss_username': '<p>Please enter your username</p>',
}


def display_message(msg_key):
    # THE DECORATOR IS NEEDED TO DISABLE CACHING OF JINJA CALLS!!!
    result = Markup(msg_dict.get(msg_key, 'Something gone wrong'))
    return result
