from typing import NamedTuple

from services.schedule.date_service import DateScheduleService
from services.schedule.time_service import TimeScheduleService


class ScheduleServices(NamedTuple):
    time_service: TimeScheduleService
    date_service: DateScheduleService
