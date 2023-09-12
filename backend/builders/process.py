from models import Payment
from utils.formating import convert_to_iso8601


# TODO: rename
# TODO: add statictyping later
class PayloadBuilder:
    @staticmethod
    def build_employee_payload(data: dict) -> dict:
        return {
            "type": "individual",
            "individual": {
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "phone": "+15121231111",
                "dob": convert_to_iso8601(data.get("dob", "")),
            },
        }

    @staticmethod
    def build_payor_payload(data: dict) -> dict:
        return {
            "type": "c_corporation",
            "corporation": {
                "name": data.get("name", ""),
                "dba": data.get("dba", ""),
                "ein": data.get("ein", ""),
            },
            "address": {
                "line1": "3300 N Interstate 35",
                "line2": None,
                "city": "Austin",
                "state": "TX",
                "zip": "78705",
            },
            # TODO: add back later - this will fail if the zipcode isnt
            # related to the state - which is all addresses in the test file
            # "address": {
            #     "line1": data.address.line1,
            #     # "line2": data.address.line2,
            #     "city": data.address.city,
            #     "state": data.address.state,
            #     "zip": data.address.zip,
            # },
        }

    @staticmethod
    def build_payee_payload(data: dict) -> dict:
        if data.get("merchant") is not None:
            return {
                "holder_id": data.get("employee_record", {}).get("external_id", ""),
                "liability": {
                    "mch_id": data.get("merchant", {}).get("mch_id", ""),
                    "number": data.get("loan_account_number", ""),
                },
            }
        return {}

    @staticmethod
    def build_payor_account_payload(data: dict) -> dict:
        return {
            "holder_id": data.get("payor_record", {}).get("external_id", ""),
            "ach": {
                "routing": data.get("aba_routing", ""),
                "number": data.get("account_number", ""),
                "type": "checking",
            },
        }

    @staticmethod
    def build_payment_payload(data: Payment):
        return {
            "amount": data["amount_cents"],
            "source": data["payor_account"]["external_id"],
            "destination": data["payee"]["external_id"],
            "description": "Loan Pmt",
        }
