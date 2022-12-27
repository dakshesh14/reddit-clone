from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user = token.user
        return user
    except Exception as e:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token = None
            for header in scope['headers']:
                if header[0] == b'authorization':
                    token = header[1].decode()
                    break

        except ValueError:
            token_key = None

        scope['user'] = AnonymousUser() if token is None else await get_user(token)
        return await super().__call__(scope, receive, send)
