from zipfile import BadZipfile

import openpyxl
from openpyxl.utils.datetime import from_excel


class ScheduleFile:
    LAST_NAME: int = 1
    FIRST_NAME: int = 2
    SURNAME: int = 3
    ROLE: int = 4
    DAY: int = 5
    TIME_START: int = 6
    TIME_FINISH: int = 7


def import_schedule(request) -> dict:
    """Import transactions and categories from xlxs file."""
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
    workbook.active = 0
    sheet = workbook.active
    rows = sheet.max_row
    employees = {}
    for row in range(1, rows + 1):
        last_name = sheet.cell(
            row=row,
            column=ScheduleFile.LAST_NAME,
        ).value
        first_name = sheet.cell(
            row=row,
            column=ScheduleFile.FIRST_NAME,
        ).value
        surname = sheet.cell(
            row=row,
            column=ScheduleFile.SURNAME,
        ).value
        role = sheet.cell(
            row=row,
            column=ScheduleFile.ROLE,
        ).value
        day = from_excel(
            sheet.cell(
                row=row,
                column=ScheduleFile.DAY,
            ).value,
        )
        time_start = sheet.cell(
            row=row,
            column=ScheduleFile.TIME_START,
        ).value
        time_finish = sheet.cell(
            row=row,
            column=ScheduleFile.TIME_FINISH,
        ).value
        if not all(
            [last_name, first_name, surname, role, day, time_start, time_finish]
        ):
            return {
                "message": "Присутствуют пропущенные значения",
            }
        employee = (last_name, first_name, surname, role)
        if employee not in employees:
            employees[employees] = set()
        employees[employees].add((day, time_start, time_finish))
    for employee, schedule in employees.items():
        for item in schedule:
            pass
