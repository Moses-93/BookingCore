from fastapi import APIRouter, status
from src.api.v1.endpoints.user import UserHandler
from src.schemas.user import UserResponse


class UserRouter:
    def __init__(self, user_handler: UserHandler):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self._registry_router(user_handler)

    def _registry_router(self, handler: UserHandler):
        self.router.add_api_route(
            "/",
            handler.get_user,
            response_model=UserResponse,
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/",
            handler.create_user,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/masters/",
            handler.link_master_to_user,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/",
            handler.delete_user,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["DELETE"],
        )
