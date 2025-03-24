from core.config import settings
from services.payments.payment_service import PaymentService
from services.payments.wayforpay.wayforpay_callback import WayForPayCallbackHandler
from services.payments.wayforpay.wayforpay_manager import WayForPayManager
from services.payments.wayforpay.wayforpay_payment_processor import (
    WayForPayPaymentProcessor,
)
from services.payments.wayforpay.wayforpay_signature import WayForPaySignature


def create_wfp_manager(payment_service: PaymentService) -> WayForPayManager:
    wayforpay_signature = WayForPaySignature(settings.merchant_secret_key)
    wayforpay_callback_handler = WayForPayCallbackHandler(wayforpay_signature)
    wayforpay_payment_processor = WayForPayPaymentProcessor(
        wayforpay_signature, settings.merchant_account
    )
    return WayForPayManager(
        wayforpay_signature,
        wayforpay_callback_handler,
        wayforpay_payment_processor,
        payment_service,
    )
