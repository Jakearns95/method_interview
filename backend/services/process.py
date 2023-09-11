from typing import Optional
from builders.process import PayloadBuilder
from services.method import MethodService
from models import Employee, Payee, Payor, Payment, BatchFile, PayorAccount
import xmltodict
import re
from pymongo import MongoClient
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv(".env.localdev")
DB_URL = os.environ.get("DB_URL")

# Things to do
# Create db session function
# Create way to get correct payee information by merchant - filter by plaid id
# Create api calls for each type of model - look into breaking up payor
# Hard code phone number
# create workers to handle rate limiting and background tasks with retry logic
# create endpoints for querying data

xml_content = """
    <root>
        <row>
        <Employee>
            <DunkinId>EMP-a7f138d9-1885-43db-b5c7-6b7c09020b4f</DunkinId>
            <DunkinBranch>BRC-bbfbdfe5-0173-4613-8b07-aadb828e67f6</DunkinBranch>
            <FirstName>Ariel</FirstName>
            <LastName>Hayes</LastName>
            <DOB>03-26-1987</DOB>
            <PhoneNumber>+14594036784</PhoneNumber>
        </Employee>
        <Payor>
            <DunkinId>CORP-7dc67e67-e879-4da0-8fee-7d14ba4752b8</DunkinId>
            <ABARouting>403911437</ABARouting>
            <AccountNumber>40909581</AccountNumber>
            <Name>Dunkin' Donuts LLC</Name>
            <DBA>Dunkin' Donuts</DBA>
            <EIN>32120240</EIN>
            <Address>
                <Line1>999 Hayes Lights</Line1>
                <City>Kerlukemouth</City>
                <State>IA</State>
                <Zip>67485</Zip>
            </Address>
        </Payor>
        <Payee>
            <PlaidId>ins_114108</PlaidId>
            <LoanAccountNumber>04807469</LoanAccountNumber>
        </Payee>
        <Amount>$8.15</Amount>
    </row>
    <row>
        <Employee>
            <DunkinId>EMP-a2c0b94b-8152-497f-81b2-154de316b5fe</DunkinId>
            <DunkinBranch>BRC-2d047a52-d2d0-4af0-88d4-f60cad1e613c</DunkinBranch>
            <FirstName>Fletcher</FirstName>
            <LastName>Rowe</LastName>
            <DOB>12-13-2002</DOB>
            <PhoneNumber>+16385328761</PhoneNumber>
        </Employee>
        <Payor>
            <DunkinId>CORP-a9804e0b-e8b0-4837-8bbe-aabafcd483dd</DunkinId>
            <ABARouting>547414133</ABARouting>
            <AccountNumber>93785544</AccountNumber>
            <Name>Dunkin' Donuts LLC</Name>
            <DBA>Dunkin' Donuts</DBA>
            <EIN>32120240</EIN>
            <Address>
                <Line1>999 Hayes Lights</Line1>
                <City>Kerlukemouth</City>
                <State>IA</State>
                <Zip>67485</Zip>
            </Address>
        </Payor>
        <Payee>
            <PlaidId>ins_116945</PlaidId>
            <LoanAccountNumber>39157047</LoanAccountNumber>
        </Payee>
        <Amount>$1.56</Amount>
    </row>
    <row>
        <Employee>
            <DunkinId>EMP-1e4f673d-d683-4597-958c-cb9cc4689653</DunkinId>
            <DunkinBranch>BRC-5713fc98-f3fe-4a69-b9f2-f29ab079b917</DunkinBranch>
            <FirstName>Lindsay</FirstName>
            <LastName>Yundt</LastName>
            <DOB>02-20-1996</DOB>
            <PhoneNumber>+14727956066</PhoneNumber>
        </Employee>
        <Payor>
            <DunkinId>CORP-55988522-7698-46ba-bddd-4bc2956a6bb4</DunkinId>
            <ABARouting>030748921</ABARouting>
            <AccountNumber>93347373</AccountNumber>
            <Name>Dunkin' Donuts LLC</Name>
            <DBA>Dunkin' Donuts</DBA>
            <EIN>32120240</EIN>
            <Address>
                <Line1>999 Hayes Lights</Line1>
                <City>Kerlukemouth</City>
                <State>IA</State>
                <Zip>67485</Zip>
            </Address>
        </Payor>
        <Payee>
            <PlaidId>ins_116861</PlaidId>
            <LoanAccountNumber>68777667</LoanAccountNumber>
        </Payee>
        <Amount>$6.72</Amount>
    </row>
    <row>
        <Employee>
            <DunkinId>EMP-ac719fbd-0a27-4db9-9285-ee2a8e6bece4</DunkinId>
            <DunkinBranch>BRC-52b071ba-5b35-4743-b219-40230551cd8c</DunkinBranch>
            <FirstName>Aurelia</FirstName>
            <LastName>Metz</LastName>
            <DOB>07-27-2003</DOB>
            <PhoneNumber>+16019260414</PhoneNumber>
        </Employee>
        <Payor>
            <DunkinId>CORP-55988522-7698-46ba-bddd-4bc2956a6bb4</DunkinId>
            <ABARouting>030748921</ABARouting>
            <AccountNumber>93347373</AccountNumber>
            <Name>Dunkin' Donuts LLC</Name>
            <DBA>Dunkin' Donuts</DBA>
            <EIN>32120240</EIN>
            <Address>
                <Line1>999 Hayes Lights</Line1>
                <City>Kerlukemouth</City>
                <State>IA</State>
                <Zip>67485</Zip>
            </Address>
        </Payor>
        <Payee>
            <PlaidId>ins_116944</PlaidId>
            <LoanAccountNumber>00299532</LoanAccountNumber>
        </Payee>
        <Amount>$1.58</Amount>
    </row>
    <row>
        <Employee>
            <DunkinId>EMP-000285fa-d544-4bf6-8e3b-4513786c01d6</DunkinId>
            <DunkinBranch>BRC-b19e8df1-77b7-40f4-a290-a909eb741e5b</DunkinBranch>
            <FirstName>Uriah</FirstName>
            <LastName>Krajcik</LastName>
            <DOB>09-06-2003</DOB>
            <PhoneNumber>+15733534238</PhoneNumber>
        </Employee>
        <Payor>
            <DunkinId>CORP-1f5ba4e7-926a-47c5-9031-b07ad1dd6261</DunkinId>
            <ABARouting>181222943</ABARouting>
            <AccountNumber>41927033</AccountNumber>
            <Name>Dunkin' Donuts LLC</Name>
            <DBA>Dunkin' Donuts</DBA>
            <EIN>32120240</EIN>
            <Address>
                <Line1>999 Hayes Lights</Line1>
                <City>Kerlukemouth</City>
                <State>IA</State>
                <Zip>67485</Zip>
            </Address>
        </Payor>
        <Payee>
            <PlaidId>ins_108798</PlaidId>
            <LoanAccountNumber>48380432</LoanAccountNumber>
        </Payee>
        <Amount>$10.08</Amount>
    </row>
    </root>
    """


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
        batch = BatchFile(content=xml_content)
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
        if not existing_data:
            external_status, external_id = self.call_third_party_api(
                data, collection_name
            )
            updated_data["external_status"] = external_status
            updated_data["external_id"] = external_id

            collection.replace_one(
                {"_id": updated_data["_id"]}, updated_data, upsert=True
            )

        return updated_data

    def create_payment_record(self, data: Payment, batch_id: str):
        collection = self.db["payments"]
        data_dict = data.dict()
        data_dict["batch_id"] = batch_id

        collection.insert_one(data_dict)

    def process_xml(self, xml_content: str):
        data = xmltodict.parse(xml_content)
        batch_id = self.save_batch_file(data)
        rows = data.get("root", {}).get("row", [])
        rows = [rows] if not isinstance(rows, list) else rows

        for row in rows:
            row = self._recursive_snake_case(row)
            employee = Employee(**row["employee"])
            employee_record = self.upsert_record(employee, "employees")
            print("employee record: ", employee_record)
            payor = Payor(**row["payor"])
            payee = Payee(**row["payee"], employee_record=employee_record)
            amount = float(row["amount"].replace("$", ""))

            payor_record = self.upsert_record(payor, "payors")
            payor_account = PayorAccount(
                aba_routing=row["payor"]["aba_routing"],
                account_number=row["payor"]["account_number"],
                payor_record=payor_record,
            )

            # Create Payment instance using snake_case
            payment_data = Payment(
                employee=employee,
                payor_account=payor_account,
                payee=payee,
                amount=amount,
                batch_id=batch_id,
            )

            # Upsert all data entities
            for entity, collection_name in [
                (payor_account, "payor_account"),
                (payee, "payees"),
            ]:
                self.upsert_record(entity, collection_name)

            self.create_payment_record(payment_data, batch_id)

    def process_payments_for_batch(self, batch_id: str):
        # Fetch all payments associated with the batch_id
        payments = list(self.payments_collection.find({"batch_id": batch_id}))

        # For each payment, make the API call and update the payment record with the response
        for payment in payments:
            response = MethodService.process_payment(payment)
            updated_data = {
                "external_id": response["id"],
                "external_status": response["status"],
                "payment_metadata": response["payload"],
            }
            self.payments_collection.update_one(
                {"_id": payment["_id"]}, {"$set": updated_data}
            )

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
