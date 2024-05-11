import enum
from typing import Final


class ScheduleErrors(enum.Enum):
    BAD_FILE: Final[str] = 'Файл является битым'
    DATES_NOT_FOUND: Final[str] = 'Отсутствуют даты смен'
    EMPLOYEE_NOT_FOUND: Final[str] = 'Сотрудник не найден'
    NULLABLE_VALUES: Final[str] = 'Присутствуют пропущенные значения'
    WRONG_COLOR: Final[str] = 'Цвет обозначения деятельности не найден'
    WRONG_EMPLOYEE: Final[str] = 'Сотрудник указан не корректно'
    WRONG_EXTENSION: Final[str] = 'Файл должен иметь расширение .xlsx'
    WRONG_ROLE: Final[str] = 'Присутствует не корректная роль'


class ScheduleColors(enum.Enum):
    VACATION: Final[str] = "000000"
    SICK_LEAVE: Final[str] = "FF0000"
    WORK: Final[str] = "00FF00"
    DAY_OFF: Final[str] = "FFFF00"


class ScheduleFile(enum.Enum):
    NUMBER_EMPLOYEE: int = 0
    FULL_NAME: int = 1
    ROLE: int = 2
    START_TIME: int = 3
