from models import Employee, Payee, Payor, Payment, BatchFile
import xmltodict
from pymongo import MongoClient
from pydantic import BaseModel

# Establish a connection to the MongoDB server.
client = MongoClient(
    "mongodb+srv://method_interview:2L30JVXndSmjZVI9@methodinterview.dvn8psu.mongodb.net/methodinterview",
    27017,
)
# Choose the database you want to use (e.g., "dunkin_database").
db = client["dunkin_database"]

xml_content = """
    <root>
        <row>
            <Employee>
                <DunkinId>EMP-208c8e79-8d85-4914-9a7a-8a899e67c530</DunkinId>
                <DunkinBranch>BRC-5a32e859-e91a-490c-b4f2-bce67695f30c</DunkinBranch>
                <FirstName>Madie</FirstName>
                <LastName>Funk</LastName>
                <DOB>12-13-2000</DOB>
                <PhoneNumber>+16473020450</PhoneNumber>
            </Employee>
            <Payor>
                <DunkinId>CORP-e4025d0e-0491-49ef-8284-2738c2d0a0cf</DunkinId>
                <ABARouting>148386123</ABARouting>
                <AccountNumber>12719660</AccountNumber>
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
                <PlaidId>ins_116947</PlaidId>
                <LoanAccountNumber>91400799</LoanAccountNumber>
            </Payee>
            <Amount>$7.03</Amount>
        </row>
        <row>
            <Employee>
                <DunkinId>EMP-208c8e79-8d85-4914-9a7a-8a899e67c530</DunkinId>
                <DunkinBranch>BRC-5a32e859-e91a-490c-b4f2-bce67695f30c</DunkinBranch>
                <FirstName>Madie</FirstName>
                <LastName>Funk</LastName>
                <DOB>12-13-2000</DOB>
                <PhoneNumber>+16473020450</PhoneNumber>
            </Employee>
            <Payor>
                <DunkinId>CORP-e4025d0e-0491-49ef-8284-2738c2d0a0cf</DunkinId>
                <ABARouting>148386123</ABARouting>
                <AccountNumber>12719660</AccountNumber>
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
                <PlaidId>ins_116947</PlaidId>
                <LoanAccountNumber>91400799</LoanAccountNumber>
            </Payee>
            <Amount>$7.13</Amount>
        </row>
    </root>
    """


class DataService:
    @staticmethod
    def save_batch_file(xml_content: dict) -> str:
        collection = db["batch_files"]
        batch = BatchFile(content=xml_content)
        result = collection.insert_one(batch.dict())
        return result.inserted_id  # Return the ID of the created batch record

    @staticmethod
    def call_third_party_api(data):
        return "Status"

    @staticmethod
    def create_payment_and_notify(data: Payment, batch_id: str):
        collection = db["payments"]
        data = data.dict()
        data["batch_id"] = batch_id  # Associate the batch_id with the payment record

        # Insert data to MongoDB
        result = collection.insert_one(data)

        # Notify the third-party API only if the record was successfully created
        if result.inserted_id:
            status = DataService.call_third_party_api(data)
            # Update the payment document with the API call status
            collection.update_one(
                {"_id": result.inserted_id}, {"$set": {"api_status": status}}
            )

    @staticmethod
    def upsert_and_notify(data: BaseModel, collection_name: str):
        collection = db[collection_name]

        if collection_name == "payments":
            criteria = {
                "employee.DunkinId": data.employee.DunkinId,
                "payor.DunkinId": data.payor.DunkinId,
                "payee.PlaidId": data.payee.PlaidId,
            }
        else:
            criteria = {
                "DunkinId": data.DunkinId if hasattr(data, "DunkinId") else data.PlaidId
            }

        values = {"$set": data.dict()}

        # Upsert data to MongoDB
        result = collection.update_one(criteria, values, upsert=True)

        # Notify the third-party API
        status = DataService.call_third_party_api(data)

        # Update the document with the API call status
        if result.upserted_id or result.matched_count > 0:
            collection.update_one(criteria, {"$set": {"api_status": status}})

    @classmethod
    def process_xml(cls, xml_content: str):
        # First, save the batch and get its ID

        data = xmltodict.parse(xml_content)
        batch_id = DataService.save_batch_file(data)
        rows = data.get("root", {}).get("row", [])
        if not isinstance(rows, list):  # Handle when there's a single row
            rows = [rows]

        for row in rows:
            employee = Employee(**row["Employee"])
            payor = Payor(**row["Payor"])
            payee = Payee(**row["Payee"])
            amount = float(
                row["Amount"].replace("$", "")
            )  # Convert string amount to float

            payment_data = Payment(
                employee=employee, payor=payor, payee=payee, amount=amount
            )

            cls.upsert_and_notify(employee, "employees")
            cls.upsert_and_notify(payor, "payors")
            cls.upsert_and_notify(payee, "payees")
            cls.create_payment_and_notify(payment_data, batch_id)

    @classmethod
    def upsert_employee(cls, data: Employee):
        """Upsert employee data."""
        collection = db["employees"]
        criteria = {"_id": data.DunkinId}
        document = data.dict(by_alias=True)
        # Upsert operation.
        collection.update_one(criteria, {"$set": document}, upsert=True)

    @classmethod
    def upsert_payor(cls, data: Payor):
        """Upsert payor data."""
        collection = db["payors"]
        criteria = {"_id": data.DunkinId}
        document = data.dict(by_alias=True)
        # Upsert operation.
        collection.update_one(criteria, {"$set": document}, upsert=True)

    @classmethod
    def upsert_payee(cls, data: Payee):
        """Upsert payee data."""
        collection = db["payees"]
        criteria = {"_id": data.PlaidId}
        document = data.dict(by_alias=True)
        # Upsert operation.
        collection.update_one(criteria, {"$set": document}, upsert=True)

    @staticmethod
    def upsert_payment(data: Payment):
        collection = db["payments"]
        # The criteria here can be more comprehensive depending on your requirements.
        # For simplicity, we use the combination of all associated IDs to find a unique payment.
        criteria = {
            "employee.DunkinId": data.employee.DunkinId,
            "payor.DunkinId": data.payor.DunkinId,
            "payee.PlaidId": data.payee.PlaidId,
        }
        values = {"$set": data.dict()}
        # TODO: do we need to update this to account for multiple payments?
        collection.update_one(criteria, values, upsert=True)
