from apps.users.models import User


def check_role_employee(user: User, role: str) -> bool:
    if user.is_client:
        return False
    return user.employee.role == role
