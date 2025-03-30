from dependency_injector import containers, providers
from src.db.repository import CRUDRepository
from .feedback_service import FeedbackService
from .feedback_manager import FeedbackManager


class FeedbackContainer(containers.DeclarativeContainer):
    feedback_service = providers.Singleton(
        FeedbackService, crud_repository=CRUDRepository
    )
    feedback_manager = providers.Singleton(
        FeedbackManager, feedback_service=feedback_service
    )


def create_feedback_container():
    return FeedbackContainer()
