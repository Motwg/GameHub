import random
from string import ascii_uppercase

activities = {'cah': 'Cards Against Humanity'}
rooms = {
    '14HKE': {
        'activity': 'cah',
        'members': {},
        'password': 'Hello',
    },
    '13HKE': {
        'activity': 'cah',
        'members': {},
        'password': False,
    },
}


def generate_unique_room_code(length):
    code = ''
    while not code or code in rooms:
        code = ''.join(random.choices(ascii_uppercase, k=length))
    return code


if __name__ == '__main__':
    print(generate_unique_room_code(6))
