import logging
import hmac
import hashlib
from typing import Any, Dict


logger = logging.getLogger(__name__)


class WayForPaySignature:

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    async def generate_signature(self, params: Dict[str, Any]) -> str:
        logger.info("Створення підпису")
        """
        Generates a signature for WayForPay using HMAC-MD5.

        :param params: A dictionary with parameters for the signature (key order is important!)
        :return: Signature as a HEX string (32 characters)
        """

        sign_str = ";".join(
            (
                str(params[key])
                if not isinstance(params[key], list)
                else ";".join(map(str, params[key]))
            )
            for key in params
        ).encode("utf-8")

        signature = hmac.new(
            self.secret_key.encode(), sign_str, hashlib.md5
        ).hexdigest()
        return signature

    async def verify_signature(self, callback: Dict[str, Any]) -> bool:
        """
        Checks the signature from WayForPay.

        :param callback: A dictionary with parameters for the signature (key order is important!)
        :return: True if the signature is valid, otherwise False
        """
        received_signature = callback["merchantSignature"]
        params = {
            "merchantAccount": callback["merchantAccount"],
            "orderReference": callback["orderReference"],
            "amount": callback["amount"],
            "currency": callback["currency"],
            "authCode": callback["authCode"],
            "cardPan": callback["cardPan"],
            "transactionStatus": callback["transactionStatus"],
            "reasonCode": callback["reasonCode"],
        }

        generated_signature = self.generate_signature(params)
        logger.info(f"generated_signature: {generated_signature}")
        return generated_signature == received_signature
