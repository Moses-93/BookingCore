import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.dependencies import get_current_user, get_db
from db.repository import crud
from db.models.feedback import Feedback
from db.models.user import User
from schemas.feedback import FeedbackCreate, FeedbackResponse
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])


@router.get("/", response_model=List[FeedbackResponse], status_code=status.HTTP_200_OK)
@requires_role(["master", "client"])
async def get_feedback(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    feedback_records = await crud.read(model=Feedback, session=db)

    for feedback in feedback_records:
        feedback.name = feedback.user.name

    logger.info(f"Feedback with names: {feedback_records}")
    return feedback_records


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback: FeedbackCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    (user,) = user
    exists_fields = feedback.model_dump(exclude_unset=True)
    exists_fields["user_id"] = user.id
    logger.info(f"Creating feedback: {exists_fields}")
    result = await crud.create(
        model=Feedback,
        session=db,
        **exists_fields,
    )
    ensure_resource_exists(
        result, status_code=400, message="Invalid data for feedback creation"
    )
    return result
