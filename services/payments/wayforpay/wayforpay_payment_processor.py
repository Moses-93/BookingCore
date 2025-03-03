import logging
import json
import uuid
from typing import Any, Dict, List, Union
from time import time

from .wayforpay_signature import WayForPaySignature
from ...http_client import HTTPClient


logger = logging.getLogger(__name__)


class WayForPayPaymentProcessor:

    wfp_url = "https://api.wayforpay.com/api"
    service_url = "https://0476-185-70-18-65.ngrok-free.app/api/v1/payments/callback/"

    def __init__(self, signature_manager: WayForPaySignature, merchant_account: str):
        self.signature_manager = signature_manager
        self.merchant_account = merchant_account

    async def create_payment_link(self, payment_data: Dict[str, Any]) -> str:
        """
        Creates a payment link using WayForPay API.

        Parameters:
        payment_data (Dict[str, Any]): A dictionary containing payment details.

        Returns:
        str: The payment link URL. Raises an exception if the payment link cannot be created.
        """

        logger.info("Create a payment link for payment")
        headers = {"Content-Type": "application/json"}
        async with HTTPClient() as client:

            response = await client.post(
                self.wfp_url, data=json.dumps(payment_data), headers=headers
            )
            response_data = response.json()
            logger.info(f"response:{response_data} | type:{type(response_data)}")

        if response_data.get("invoiceUrl"):
            return response_data["invoiceUrl"]
        else:
            raise Exception(f"Помилка WayForPay: {response_data}")

    def create_order_reference(self) -> str:
        """
        Generates a unique order reference for WayForPay transactions.

        The order reference is a combination of the prefix "SUB-" and a randomly generated hexadecimal string of length 10.
        This reference is used to uniquely identify each payment transaction.

        Parameters:
        None

        Returns:
        str: A unique order reference in the format "SUB-{hexadecimal_string}".
        """
        order_reference = f"SUB-{uuid.uuid4().hex[:10]}"
        return order_reference

    async def create_invoice(
        self, plan_price: Union[int, float]
    ) -> Dict[str, Union[str, int, float, List[str], List[int]]]:
        """
        Creates a payment invoice for the specified plan price using WayForPay API.

        Parameters:
        plan_price (Union[int, float]): The price of the subscription plan.

        Returns:
        Dict[str, Union[str, int, float, List[str], List[int]]]: A dictionary containing the payment invoice parameters.
        The dictionary includes the following keys:
        - merchantAccount: The merchant account identifier.
        - merchantDomainName: The merchant domain name.
        - orderReference: A unique order reference for the transaction.
        - orderDate: The date and time of the transaction.
        - amount: The total amount to be paid.
        - currency: The currency of the payment.
        - productName: A list of product names.
        - productCount: A list of product quantities.
        - productPrice: A list of product prices.
        - transactionType: The type of transaction (CREATE_INVOICE).
        - merchantSignature: The merchant signature for authentication.
        - apiVersion: The API version.
        - language: The language of the payment page.
        - serviceUrl: The URL for the payment callback service.
        """
        logger.info("Starting to create an invoice")

        params = {
            "merchantAccount": self.merchant_account,
            "merchantDomainName": "t.me/book_easy_bot",
            "orderReference": self.create_order_reference(),
            "orderDate": int(time()),
            "amount": int(plan_price),
            "currency": "UAH",
            "productName": ["Оплата за підписку на Telegram бота"],
            "productCount": [1],
            "productPrice": [str(plan_price)],
        }

        signature = self.signature_manager.generate_signature(params)

        params["transactionType"] = "CREATE_INVOICE"
        params["merchantSignature"] = signature
        params["apiVersion"] = 2
        params["language"] = "UA"
        params["serviceUrl"] = self.service_url
        return params
