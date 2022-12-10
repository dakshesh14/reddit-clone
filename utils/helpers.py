import uuid
import random

# google
from google.oauth2 import id_token
from google.auth.transport import requests

# local
from .constants import prefixes, suffixes, pre_prefixes


def get_uuid():
    return str(uuid.uuid4())[:8]


def get_random_name() -> str:
    name = f"{random.choice(prefixes)}{random.choice(suffixes)}"
    if random.random() < 0.2:
        name = f"{random.choice(pre_prefixes)}{name}"
    return name


def validate_google_token(token, client_id):

    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), client_id
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None

        data = {
            'email': id_info['email'],
        }

        return data

    except ValueError:
        return None
