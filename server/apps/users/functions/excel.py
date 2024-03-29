from datetime import (
    datetime,
    time,
    timedelta,
)
from zipfile import BadZipfile

import openpyxl

from apps.users.constants import (
    ScheduleColors,
    ScheduleErrors,
    ScheduleFile,
)
from apps.users.models import Employee, Schedule
from apps.users.serializers import EmployeeScheduleSerializer


def import_schedule(request) -> list:
    if request.data['file'].name.split('.')[-1] != 'xlsx':
        return {
            'file': ScheduleErrors.WRONG_EXTENSION.value,
        }
    try:
        workbook = openpyxl.reader.excel.load_workbook(
            request.data['file'],
            read_only=True,
        )
    except BadZipfile:
        return {
            'file': ScheduleErrors.BAD_FILE.value,
        }
    restaurant = request.user.employee.restaurant
    workbook.active = 0
    sheet = workbook.active
    dates = []
    rows = []
    for index, row in enumerate(sheet.iter_rows()):
        if index == 0:
            for cell in row[ScheduleFile.START_TIME.value:]:
                if cell.value:
                    dates.append(cell.value)
        else:
            if row[ScheduleFile.FULL_NAME.value].value is not None:
                rows.append(row)

    max_column = ScheduleFile.START_TIME.value + len(dates) * 2
    schedule_items = []
    for row in rows:
        row = row[:max_column]
        role = row[ScheduleFile.ROLE.value].value
        if role not in Employee.Roles.labels:
            return {
                "file": f"{ScheduleErrors.WRONG_ROLE.value} {role}",
            }
        role_index = Employee.Roles.labels.index(role)
        full_name = row[ScheduleFile.FULL_NAME.value].value
        employee_info = full_name.split()
        if len(employee_info) < 3:
            return {
                'file': f"{ScheduleErrors.WRONG_EMPLOYEE.value} '{full_name}'",
            }
        obj = Employee.objects.filter(
            user__last_name=employee_info[0],
            user__first_name=employee_info[1],
            user__surname=employee_info[2],
            role=Employee.Roles.names[role_index],
            restaurant=restaurant,
        )
        if not obj.exists():
            return {
                "file": f"{ScheduleErrors.EMPLOYEE_NOT_FOUND.value} '{full_name} {role}'",
            }
        employee = obj.first()
        date_index = 0
        times = row[ScheduleFile.START_TIME.value:]
        for index in range(0, len(times), 2):
            time_start = times[index].value if times[index].value else time(0, 0, 0)
            time_finish = times[index + 1].value if times[index + 1].value else time(23, 59, 59)
            date_from_file = dates[date_index]

            if isinstance(times[index].fill.start_color.index, int):
                return {
                    "file": ScheduleErrors.WRONG_COLOR.value,
                }
            alpha = times[index].fill.start_color.index[:2]
            color = times[index].fill.start_color.index[2:]
            name = ScheduleColors.WORK.name
            if alpha == "FF":
                for field in ScheduleColors:
                    if field.value == color:
                        name = field.name
                        break
                else:
                    return {
                        "file": ScheduleErrors.WRONG_COLOR.value,
                    }

            add_days = 0
            if time_start > time_finish:
                add_days = 1
            start = datetime.combine(date_from_file, time_start)
            end = datetime.combine(
                date_from_file + timedelta(days=add_days),
                time_finish,
            )

            query = Schedule.objects.filter(
                time_start=start,
                time_finish=end,
                employee=employee,
                type=name,
            )
            if not query.exists():
                to_create_item = {
                    "time_start": start,
                    "time_finish": end,
                    "employee": employee.id,
                    "type": name,
                }
                serializer = EmployeeScheduleSerializer(data=to_create_item)
                serializer.is_valid(raise_exception=True)
                schedule_items.append(serializer)
            date_index += 1
    created_items = []
    for serializer in schedule_items:
        serializer.save()
        created_items.append(serializer.data)
    return created_items
