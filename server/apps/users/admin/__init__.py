from .client import ClientAdmin
from .employee import EmployeeAdmin
from .schedule import ScheduleAdmin
from .user import UserAdminNew as UserAdmin

__all__ = (UserAdmin, ClientAdmin, ScheduleAdmin, EmployeeAdmin)
