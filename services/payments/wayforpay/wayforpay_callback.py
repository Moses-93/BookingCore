import logging
from typing import Any, Dict
from time import time
from .wayforpay_signature import WayForPaySignature


logger = logging.getLogger(__name__)


class WayForPayCallbackHandler:

    def __init__(self, signature_manager: WayForPaySignature):
        self.signature_manager = signature_manager

    async def verify_callback(self, callback: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting WayForPay signature verification")
        is_signature_valid = await self.signature_manager.verify_signature(callback)
        logger.info(f"Signature valid: {is_signature_valid}")

        status = "accept" if is_signature_valid else "decline"
        params = {
            "orderReference": callback["orderReference"],
            "status": status,
            "time": int(time()),
        }
        signature = await self.signature_manager.generate_signature(params)
        params["signature"] = signature
        return params
