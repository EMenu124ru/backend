from datetime import date
from zipfile import BadZipfile

import openpyxl
from django.shortcuts import get_object_or_404

from apps.users.models import Employee, Schedule
from apps.users.serializers import EmployeeScheduleSerializer


class ScheduleFile:
    LAST_NAME: int = 0
    FIRST_NAME: int = 1
    SURNAME: int = 2
    ROLE: int = 3
    DAY: int = 4
    TIME_START: int = 5
    TIME_FINISH: int = 6


def import_schedule(request) -> list:
    if request.data['file'].name.split('.')[-1] != 'xlsx':
        return {
            'file': 'Файл должен иметь расширение .xlsx',
        }
    try:
        workbook = openpyxl.reader.excel.load_workbook(
            request.data['file'],
            read_only=True,
        )
    except BadZipfile:
        return {
            'file': 'Файл является битым',
        }
    sheet = workbook.active
    employees = {}
    for row in sheet.iter_rows(min_row=2):
        last_name = row[ScheduleFile.LAST_NAME].value
        first_name = row[ScheduleFile.FIRST_NAME].value
        surname = row[ScheduleFile.SURNAME].value
        role = row[ScheduleFile.ROLE].value
        day = row[ScheduleFile.DAY].value
        time_start = row[ScheduleFile.TIME_START].value
        time_finish = row[ScheduleFile.TIME_FINISH].value
        if not all(
            [last_name, first_name, surname, role, day, time_start, time_finish]
        ):
            return {
                "file": "Присутствуют пропущенные значения",
            }
        employee = (last_name, first_name, surname, role)
        if employee not in employees:
            employees[employee] = set()
        employees[employee].add((day, time_start, time_finish))
    schedule_items = []
    for employee, schedule in employees.items():
        try:
            index = Employee.Roles.labels.index(employee[3])
        except ValueError:
            return {
                "file": f"Присутствует не корректная роль {employee[3]}",
            }
        employee = get_object_or_404(
            Employee,
            user__last_name=employee[0],
            user__first_name=employee[1],
            user__surname=employee[2],
            role=Employee.Roles.names[index],
        )
        to_create = []
        for item in schedule:
            if not Schedule.objects.filter(
                day=item[0],
                time_start=item[1],
                time_finish=item[2],
                employee=employee,
            ).exists():
                to_create_item = {
                    "day": date(item[0].year, item[0].month, item[0].day),
                    "time_start": item[1],
                    "time_finish": item[2],
                    "employee": employee.id,
                }
                serializer = EmployeeScheduleSerializer(data=to_create_item)
                serializer.is_valid(raise_exception=True)
                to_create.append(serializer)

        for serializer in to_create:
            serializer.save()
            schedule_items.append(serializer.data)
    return schedule_items
