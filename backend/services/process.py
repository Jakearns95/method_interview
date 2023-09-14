import json
import os
import re
from datetime import datetime
from typing import Any, List, Optional

import xmltodict
from bson import ObjectId
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel
from pymongo import MongoClient

from builders.process import PayloadBuilder
from models import BatchFile, Employee, Payee, Payment, Payor, PayorAccount
from services.method import MethodService
from utils.logging import init_logger

logger = init_logger(__name__)

load_dotenv(".env.localdev")
DB_URL = os.environ.get("DB_URL")


# TODO move later
class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class DataService:
    def __init__(self):
        self._initialize_database_connection()
        self.payments_collection = self.db["payments"]
        self.merchants_collection = self.db["merchants"]

    def _initialize_database_connection(self):
        self.client = MongoClient(DB_URL, 27017)
        self.db = self.client["dunkin_database"]

    @staticmethod
    def _get_collection_filter(data: BaseModel, collection_name: str) -> dict:
        filters = {
            "payors": "dunkin_id",
            "employees": "dunkin_id",
            "payees": "plaid_id",
            "payor_account": "account_number",
        }
        attribute = filters.get(collection_name)
        if attribute and hasattr(data, attribute):
            return {attribute: getattr(data, attribute)}
        return {}

    def save_batch_file(self, xml_content: dict) -> str:
        batch = BatchFile(content=xml_content, date=datetime.now().strftime("%m-%d-%y"))
        batch_id = self.db["batch_files"].insert_one(batch.dict()).inserted_id

        # After creating batch file, fetch and store merchant data
        self._update_merchants()

        return batch_id

    def _update_merchants(self):
        """Retrieve all merchants using MethodService and update the single merchant document."""
        merchants_data = MethodService.get_merchants()

        # Using a static unique identifier for the merchant data record.
        # This ensures we are always updating the same record.
        merchant_record_identifier = "unique_merchant_record"

        self.merchants_collection.update_one(
            {"record_id": merchant_record_identifier},
            {"$set": {"data": merchants_data}},
            upsert=True,
        )

    def _find_merchant_by_plaid_id(self, plaid_id: str) -> Optional[dict]:
        """Return the merchant associated with the given plaid_id."""
        merchant_record_identifier = "unique_merchant_record"
        merchant_document = self.merchants_collection.find_one(
            {"record_id": merchant_record_identifier}
        )

        if not merchant_document:
            return None

        for merchant in merchant_document.get("data", []):
            if plaid_id in merchant.get("provider_ids", {}).get("plaid", []):
                return merchant
        return None

    @staticmethod
    def call_third_party_api(data: BaseModel, collection_name: str):
        method_map = {
            "employees": {
                "method": MethodService.create_entity,
                "payload_fn": PayloadBuilder.build_employee_payload,
            },
            "payors": {
                "method": MethodService.create_entity,
                "payload_fn": PayloadBuilder.build_payor_payload,
            },
            "payees": {
                "method": MethodService.create_account,
                "payload_fn": PayloadBuilder.build_payee_payload,
            },
            "payor_account": {
                "method": MethodService.create_account,
                "payload_fn": PayloadBuilder.build_payor_account_payload,
            },
        }

        collection_info = method_map.get(collection_name)
        if not collection_info:
            raise ValueError(f"Unknown collection_name: {collection_name}")

        payload = collection_info["payload_fn"](data)
        response = collection_info["method"](payload)
        status = response.get("status")
        id = response.get("id")

        return status, id

    def upsert_record(self, data: BaseModel, collection_name: str):
        collection = self.db[collection_name]
        filter_criteria = self._get_collection_filter(data, collection_name)

        existing_data = collection.find_one(filter_criteria)
        updated_data = collection.find_one_and_update(
            filter_criteria, {"$set": data.dict()}, upsert=True, return_document=True
        )

        if collection_name == "payees" and hasattr(data, "plaid_id"):
            merchant_data = self._find_merchant_by_plaid_id(data.plaid_id)
            if merchant_data:
                updated_data["merchant"] = merchant_data
                collection.replace_one(
                    {"_id": updated_data["_id"]}, updated_data, upsert=True
                )

        # If new record, notify third-party API
        # If we fail to make an API call, no user is created
        if not existing_data:
            try:
                external_status, external_id = self.call_third_party_api(
                    updated_data, collection_name
                )
                updated_data["external_status"] = external_status
                updated_data["external_id"] = external_id

                collection.replace_one(
                    {"_id": updated_data["_id"]}, updated_data, upsert=True
                )
            except ValueError as e:
                logger.exception(e)

        return updated_data

    def create_payment_record(self, data: Payment, batch_id: str):
        collection = self.db["payments"]
        data_dict = data.dict()
        data_dict["batch_id"] = batch_id

        collection.insert_one(data_dict)

    def process_xml(self, xml_content: str) -> List:
        try:
            data = xmltodict.parse(xml_content)
            print("data", data)
            batch_id = self.save_batch_file(data)
            rows = data.get("root", {}).get("row", [])
            rows = [rows] if not isinstance(rows, list) else rows

            for row in rows:
                row = self._recursive_snake_case(row)
                employee = Employee(**row["employee"])
                employee_record = self.upsert_record(employee, "employees")
                payor = Payor(**row["payor"])
                payee = Payee(**row["payee"], employee_record=employee_record)
                amount = float(row["amount"].replace("$", "")) * 100

                payor_record = self.upsert_record(payor, "payors")
                payor_account = PayorAccount(
                    aba_routing=row["payor"]["aba_routing"],
                    account_number=row["payor"]["account_number"],
                    payor_record=payor_record,
                )
                payor_account_record = self.upsert_record(
                    payor_account, "payor_account"
                )
                payee_record = self.upsert_record(payee, "payees")

                # if there is an incorrect merchant, skip a payment record
                if payee_record.get("merchant") is not None:
                    # Create Payment instance using snake_case
                    payment_data = Payment(
                        employee=employee,
                        payor_account=payor_account_record,
                        payee=payee_record,
                        amount_cents=amount,
                        batch_id=batch_id,
                    )

                    self.create_payment_record(payment_data, batch_id)

            pending_payments = self.get_all_payments_by_batch(batch_id)
            return self.convert_json(pending_payments)
        except Exception as e:
            logger.exception(e)

    def process_payments_for_batch(self, batch_id: str):
        # Fetch all payments associated with the batch_id
        payments = self.get_all_payments_by_batch(batch_id)

        # For each payment, make the API call and update the payment record with the response
        for payment in payments:
            try:
                payload = PayloadBuilder.build_payment_payload(payment)
                response = MethodService.process_payment(payload)
                updated_data = {
                    "external_id": response["id"],
                    "external_status": response["status"],
                    "payment_metadata": response,
                }
                self.payments_collection.update_one(
                    {"_id": payment["_id"]}, {"$set": updated_data}
                )
            except Exception as e:
                logger.exception(e)
                continue

    @staticmethod
    def to_snake_case(string: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def _recursive_snake_case(self, data: dict) -> dict:
        """Recursively convert the keys of the dictionary to snake_case."""
        new_data = {}
        for key, value in data.items():
            snake_key = self.to_snake_case(key)
            if isinstance(value, dict):
                new_data[snake_key] = self._recursive_snake_case(value)
            else:
                new_data[snake_key] = value
        return new_data

    def get_all_payments_by_batch(self, batch_id: str) -> List:
        return list(self.payments_collection.find({"batch_id": ObjectId(batch_id)}))

    def get_all_batch_records(self) -> List:
        records = list(self.db["batch_files"].find({}, {"date": 1, "_id": 1}))

        serialized_data = JSONEncoder().encode(records)

        # Convert the serialized string back to a Python dictionary.
        return json.loads(serialized_data)

    def _build_initial_pipeline(self, batch_id=None):
        pipeline = []
        if batch_id:
            pipeline.append({"$match": {"batch_id": ObjectId(batch_id)}})
        return pipeline

    def _execute_aggregation(self, pipeline):
        return list(self.payments_collection.aggregate(pipeline))

    def get_total_by_corp(self, batch_id=None):
        pipeline = self._build_initial_pipeline(batch_id)
        pipeline.append(
            {
                "$group": {
                    "_id": "$payor_account.payor_record.dunkin_id",
                    "total_amount_cents": {"$sum": "$amount_cents"},
                }
            }
        )
        result = self._execute_aggregation(pipeline)
        return self.convert_json(result)

    def get_total_by_branch(self, batch_id=None):
        pipeline = self._build_initial_pipeline(batch_id)
        pipeline.append(
            {
                "$group": {
                    "_id": "$employee.dunkin_branch",
                    "total_amount_cents": {"$sum": "$amount_cents"},
                }
            }
        )
        result = self._execute_aggregation(pipeline)
        return self.convert_json(result)

    def get_all_payments(self, batch_id=None):
        filter_criteria = {}
        if batch_id:
            filter_criteria["batch_id"] = ObjectId(batch_id)

        records = list(
            self.payments_collection.find(
                filter_criteria,
                {
                    "_id": 1,
                    "amount_cents": 1,
                    "external_status": 1,
                    "payment_metadata": 1,
                },
            )
        )
        return self.convert_json(records)

    @staticmethod
    def convert_json(data: List):
        serialized_data = JSONEncoder().encode(data)

        # Convert the serialized string back to a Python dictionary.
        return json.loads(serialized_data)
