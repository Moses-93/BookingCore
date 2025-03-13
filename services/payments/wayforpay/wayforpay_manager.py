import logging
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from typing import Dict, Any
from services.payments import (
    WayForPayCallbackHandler,
    WayForPayManager,
    WayForPayPaymentProcessor,
    WayForPaySignature,
    payment_service,
    PaymentService,
)


logger = logging.getLogger(__name__)


class WayForPayManager:

    def __init__(
        self,
        signature_manager: WayForPaySignature,
        callback_handler: WayForPayCallbackHandler,
        payment_processor: WayForPayPaymentProcessor,
        payment_service: PaymentService,
    ):
        self.signature_manager = signature_manager
        self.callback_handler = callback_handler
        self.payment_processor = payment_processor
        self.payment_service = payment_service

    async def create_payment(
        self, db: AsyncSession, plan_id: int, plan_price: float, user_id: int
    ) -> str:
        """
        Creates a payment for a given plan and user.

        This method interacts with the payment processor to create an invoice,
        store the payment details in the database, and generate a payment link.

        Parameters:
        - db (AsyncSession): The database session for asynchronous operations.
        - plan_id (int): The ID of the subscription plan.
        - plan_price (float): The price of the subscription plan.
        - user_id (int): The ID of the user.

        Returns:
        - str: The payment link generated by the payment processor.
        """
        payment_data = await self.payment_processor.create_invoice(plan_price)
        await self.payment_service.create_payment(
            db, plan_id, user_id, payment_data["orderReference"], plan_price
        )
        return await self.payment_processor.create_payment_link(payment_data)

    async def handle_callback(self, session, callback_data) -> Dict[str, Any]:
        """
        Handles the callback received from WayForPay payment processor.

        This method verifies the callback data using the callback handler,
        processes the payment if the signature is confirmed, and logs the status.

        Parameters:
        - session (AsyncSession): The database session for asynchronous operations.
        - callback_data (Dict[str, Any]): The callback data received from WayForPay.

        Returns:
        - Dict[str, Any]: The response from the callback handler.
        """
        response = await self.callback_handler.verify_callback(callback_data)
        if response["status"] == "accept":
            logger.info("The signature is confirmed. Payment verification starts.")
            await self.payment_service.process_payment(
                session,
                callback_data["orderReference"],
                callback_data["paymentSystem"],
                callback_data["transactionStatus"],
            )
        else:
            logger.error("Invalid signature received. Returning 'decline' status.")
        return response


merchant_secret_key = settings.merchant_secret_key
merchant_account = settings.merchant_account
wayforpay_signature = WayForPaySignature(merchant_secret_key)
wayforpay_callback_handler = WayForPayCallbackHandler(wayforpay_signature)
wayforpay_payment_processor = WayForPayPaymentProcessor(
    wayforpay_signature, merchant_account
)
wfp_manager = WayForPayManager(
    wayforpay_signature,
    wayforpay_callback_handler,
    wayforpay_payment_processor,
    payment_service,
)
