from typing import Literal

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


def get_jwt_tokens(user: User) -> dict[Literal["access"], Literal["refresh"]]:
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
