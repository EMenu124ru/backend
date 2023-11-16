from typing import Final


class ScheduleErrors:
    WRONG_EXTENSION: Final[str] = 'Файл должен иметь расширение .xlsx'
    BAD_FILE: Final[str] = 'Файл является битым'
    NULLABLE_VALUES: Final[str] = 'Присутствуют пропущенные значения'
    WRONG_ROLE: Final[str] = 'Присутствует не корректная роль'
    EMPLOYEE_NOT_FOUND: Final[str] = 'Сотрудник не найден'


class ScheduleFile:
    LAST_NAME: int = 0
    FIRST_NAME: int = 1
    SURNAME: int = 2
    ROLE: int = 3
    DAY: int = 4
    TIME_START: int = 5
    TIME_FINISH: int = 6
