import random
import string
import hashlib
from uuid import uuid4


def get_hash_md5_for_string(string: str):
    hash = hashlib.md5(string.encode('utf-8'))
    return hash.hexdigest()


def generate_random_token():
    return str(uuid4())


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_intervals_numbers(pattern, char):
    list_emitted_at = []
    for split_string in pattern:
        ranges = [int(i) for i in split_string.split(char)]
        list_emitted_at += [
            item for item in range(ranges[0], ranges[1] + 1)
        ]
    return list_emitted_at


def get_numbers_in_str(value):
    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return int(value)

    if not isinstance(value, str):
        raise TypeError('Value must be float, int or str.')

    get_ints = [str(s) for s in value if s.isdigit()]
    if get_ints:
        return int(''.join(i for i in get_ints))
    else:
        raise TypeError('Value must be digite in str.')
