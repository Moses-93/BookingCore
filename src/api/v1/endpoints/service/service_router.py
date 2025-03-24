from typing import List
from fastapi import APIRouter, status
from api.v1.endpoints.service import ServiceHandler
from schemas import ServiceResponse


class ServiceRouter:
    def __init__(self, service_handler: ServiceHandler):
        self.router = APIRouter(prefix="/services", tags=["services"])
        self._registry_router(service_handler)

    def _registry_router(self, handler: ServiceHandler):
        self.router.add_api_route(
            "/",
            handler.get_services,
            response_model=List[ServiceResponse],
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/",
            handler.create_service,
            response_model=ServiceResponse,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/deactivate/{service_id}",
            handler.deactivate_service,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["PATH"],
        )
        self.router.add_api_route(
            "/{service_id}",
            handler.update_service,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["PATH"],
        )
