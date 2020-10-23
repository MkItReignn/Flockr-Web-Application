from utils import decode_token
from error import InputError, AccessError


def valid_channel_name(name):
    if len(name) > 20 or len(name) < 1 or name.isspace():
        raise InputError ("Channel name must consist of 1 to 20 characters long.")