from typing import List
from fastapi import APIRouter, status
from api.v1.endpoints.business_info import BusinessInfoHandler
from schemas import BusinessInfoResponse


class BusinessInfoRouter:
    def __init__(self, business_info_handler: BusinessInfoHandler):
        self.router = APIRouter(prefix="/business-info", tags=["business-info"])
        self._registry_router(business_info_handler)

    def _registry_router(self, handler: BusinessInfoHandler):
        self.router.add_api_route(
            "/",
            handler.get_business_info,
            response_model=List[BusinessInfoResponse],
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/",
            handler.create_business_info,
            response_model=BusinessInfoResponse,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/",
            handler.update_business_info,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["PATH"],
        )
