from services.schedule.date_service import DateScheduleService
from services.schedule.time_service import TimeScheduleService


class ScheduleManager:
    def __init__(
        self, date_service: DateScheduleService, time_service: TimeScheduleService
    ):
        self.date_service = date_service
        self.time_service = time_service
