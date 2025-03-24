import logging

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db, get_current_user
from decorators.permissions import requires_role

from db.models.user import User
from schemas.payment import PaymentCreate
from services.payments.wayforpay.wayforpay_manager import wfp_manager


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["master"])
async def create_payment_invoice(
    plan: PaymentCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Starting handler to create payment url")
    payment_link = await wfp_manager.create_payment(db, plan.id, plan.price, user.id)

    return payment_link


@router.post("/callback/")
async def wayforpay_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        wfp_callback = await request.json()
        logger.info(f"callback: {wfp_callback}")

        response = await wfp_manager.handle_callback(db, wfp_callback)

        logger.info(f"response_params: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing callback: {str(e)} | {e.args}")
        return {"status": "ERROR"}
