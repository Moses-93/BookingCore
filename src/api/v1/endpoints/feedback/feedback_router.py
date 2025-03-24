from typing import List
from fastapi import APIRouter, status
from src.api.v1.endpoints.feedback import FeedbackHandler
from src.schemas import FeedbackResponse


class FeedbackRouter:
    def __init__(self, feedback_handler: FeedbackHandler):
        self.router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])
        self._registry_router(feedback_handler)

    def _registry_router(self, handler: FeedbackHandler):
        self.router.add_api_route(
            "/",
            handler.get_feedback,
            response_model=List[FeedbackResponse],
            status_code=status.HTTP_200_OK,
        )
        self.router.add_api_route(
            "/",
            handler.create_feedback,
            response_model=FeedbackResponse,
            status_code=status.HTTP_201_CREATED,
        )
