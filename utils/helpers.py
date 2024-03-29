import uuid
import random


# google
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# local
from .constants import prefixes, suffixes, pre_prefixes


def get_uuid(query_length: int = 8):
    return str(uuid.uuid4())[:query_length]


def get_random_name() -> str:
    name = f"{random.choice(prefixes)}{random.choice(suffixes)}"
    if random.random() < 0.2:
        name = f"{random.choice(pre_prefixes)}{name}"
    return name


def validate_google_token(token, client_id):

    try:
        id_info = id_token.verify_oauth2_token(
            token, google_requests.Request(), client_id
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None

        data = {
            'email': id_info['email'],
        }

        return data

    except ValueError:
        return None


def get_random_identicon(seed: str):
    return f"https://avatars.dicebear.com/api/identicon/${seed}.png"


def get_random_avatar(seed: str):
    return f"https://avatars.dicebear.com/api/bottts/${seed}.png"


def get_auth_token(user):

    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
