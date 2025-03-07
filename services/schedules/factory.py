from services.user import user_tools
from tasks.task_manager import TaskManager
from .date_service import DateScheduleService
from .time_service import TimeScheduleService


class ServiceFactory:
    def __init__(self):
        self.user_tools = user_tools
        self.deactivation_task = TaskManager.Deactivation()

    def create_date_service(self) -> DateScheduleService:
        return DateScheduleService(self.user_tools, self.deactivation_task)

    def create_time_service(self) -> TimeScheduleService:
        return TimeScheduleService(self.user_tools, self.deactivation_task)