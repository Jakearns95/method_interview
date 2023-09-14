import json
import os

import requests
from dotenv import load_dotenv
from method import Method

from utils.logging import init_logger

logger = init_logger(__name__)
load_dotenv(".env.localdev")
API_KEY = os.environ.get("METHOD_API_LEY")
method = Method(env="dev", api_key=API_KEY)


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


# TODO: look into using package - having trouble with error handling/logging
class MethodService:
    """Service class for all method related calls"""

    BASE_URL = "https://dev.methodfi.com"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    @classmethod
    def _send_request(cls, endpoint: str, payload: dict):
        """Helper method to send a POST request and return the data."""
        try:
            response = requests.post(
                f"{cls.BASE_URL}/{endpoint}",
                headers=cls.HEADERS,
                data=json.dumps(payload),
            )
            # response.raise_for_status()  # Raise an HTTPError if the response contains an HTTP error status code.
            return response.json().get("data")
        except requests.RequestException as e:
            logger.exception(f"Error occurred when sending request to {endpoint}: {e}")
            raise e

    @classmethod
    def create_entity(cls, payload: dict):
        """This will create the entity for both individuals and corporations."""
        return cls._send_request("entities", payload)

    @classmethod
    def create_account(cls, payload: dict):
        """This will create the bank and liability accounts for both debits and credits."""
        return cls._send_request("accounts", payload)

    @classmethod
    def get_merchants(cls):
        """This will retrieve all the merchants in methods db."""
        try:
            merchants = method.merchants.list()
            return merchants
        except Exception as e:
            logger.exception(f"Error occurred when retrieving merchants: {e}")
            raise e

    @classmethod
    def process_payment(cls, payment: dict) -> dict:
        """Logic to call the third-party API with the payment data."""
        return cls._send_request("payments", payment)
