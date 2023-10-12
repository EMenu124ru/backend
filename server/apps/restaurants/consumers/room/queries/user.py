from channels.db import database_sync_to_async

from apps.users.models import User


class UserQueries:

    @staticmethod
    @database_sync_to_async
    def is_client(user: User) -> bool:
        return user.is_client
