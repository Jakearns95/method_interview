from method import Method
import requests

import os
from dotenv import load_dotenv
from utils.logging import init_logger
import json

logger = init_logger(__name__)
load_dotenv(".env.localdev")
API_KEY = os.environ.get("METHOD_API_LEY")
method = Method(env="dev", api_key=API_KEY)
url = "https://dev.methodfi.com/accounts"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


class MethodService:
    @classmethod
    def create_entity(cls, payload: dict):
        """This will create the entity for both individuals and corporations"""
        try:
            entity = method.entities.create(payload)

            return entity
        except Exception as e:
            print(f"Error occurred: {e}")
            raise e

    @classmethod
    def create_account(cls, payload: dict):
        """This will create the bank and liability accounts for both debits and credits"""
        print(payload)
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        print(response.status_code)
        print(response.json())
        # account = method.accounts.create(payload)
        return {"status": "success", "id": 1}

    @classmethod
    def get_merchants(cls):
        """This will retrieve all the merchants in methods db"""
        merchants = method.merchants.list()
        return merchants

    @staticmethod
    def process_payment(payment: dict) -> dict:
        # Logic to call the third-party API with the payment data
        # payment = method.payments.create(payment)
        return {"status": "success", "id": 1}
