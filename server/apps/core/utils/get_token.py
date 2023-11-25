from typing import Literal

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


def get_jwt_tokens(user: User) -> dict[Literal["access"], Literal["refresh"]]:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
