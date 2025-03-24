from fastapi import APIRouter, status
from src.api.v1.endpoints.booking import BookingHandler


class BookingRouter:
    def __init__(self, booking_handler: BookingHandler):
        self.router = APIRouter(prefix="/bookings", tags=["bookings"])
        self._registry_router(booking_handler)

    def _registry_router(self, handler: BookingHandler):
        self.router.add_api_route(
            "/", handler.get_bookings, methods=["GET"], status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/",
            handler.create_booking,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/{booking_id}",
            handler.deactivate_book,
            methods=["PATH"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
