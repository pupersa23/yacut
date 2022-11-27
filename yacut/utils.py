import random
import string

from .models import URL_map


def get_unique_short_id():
    symbol = string.ascii_lowercase + string.digits + string.ascii_uppercase
    short_link = ''.join(random.choice(symbol) for i in range(6))
    if URL_map.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link
