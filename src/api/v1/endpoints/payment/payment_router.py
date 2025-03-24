from fastapi import APIRouter, status
from api.v1.endpoints.payment import PaymentHandler


class PaymentRouter:

    def __init__(self, payment_handler: PaymentHandler):
        self.router = APIRouter(prefix="/payments", tags=["payments"])
        self._registry_router(payment_handler)

    def _registry_router(self, handler: PaymentHandler):
        self.router.add_api_route(
            "/",
            handler.create_payment_invoice,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/callback/", handler.wayforpay_callback, methods=["POST"]
        )
