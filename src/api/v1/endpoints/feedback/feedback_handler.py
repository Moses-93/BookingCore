import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_current_user, get_db
from db.models.feedback import Feedback
from db.models.user import User
from schemas.feedback import FeedbackCreate
from decorators.permissions import requires_role

logger = logging.getLogger(__name__)


class FeedbackHandler:

    def __init__(self, feedback_manager):
        self.feedback_manager = feedback_manager

    @requires_role(["master", "client"])
    async def get_feedback(
        self,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        return await self.feedback_manager.get_feedbacks(model=Feedback, session=db)

    async def create_feedback(
        self,
        feedback: FeedbackCreate,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        return await self.feedback_manager.create_feedback(db, feedback, user)
