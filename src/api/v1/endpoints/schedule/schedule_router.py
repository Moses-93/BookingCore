from typing import List
from fastapi import APIRouter, status
from api.v1.endpoints.schedule import ScheduleHandler
from schemas import DateResponse, TimeResponse


class ScheduleRouter:
    def __init__(self, schedule_handler: ScheduleHandler):
        self.router = APIRouter(prefix="/schedules", tags=["dates"])
        self._registry_router(schedule_handler)

    def _registry_router(self, handler: ScheduleHandler):
        self.router.add_api_route(
            "/dates",
            handler.get_dates,
            response_model=List[DateResponse],
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/dates",
            handler.create_date,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/dates/{date_id}",
            handler.deactivate_date,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["PATH"],
        )
        self.router.add_api_route(
            "/dates/times",
            handler.get_times,
            response_model=list[TimeResponse],
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/dates/times",
            handler.create_time,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/dates/times/{time_id}",
            handler.deactivate_time,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["PATH"],
        )
