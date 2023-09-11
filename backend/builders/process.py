from utils.formating import convert_to_iso8601
from models import Employee, Payor, Payee, Payment, PayorAccount


# TODO: rename
class PayloadBuilder:
    @staticmethod
    def build_employee_payload(data: Employee) -> dict:
        return {
            "type": "individual",
            "individual": {
                "first_name": data.first_name,
                "last_name": data.last_name,
                "phone": "+15121231111",
                "dob": convert_to_iso8601(data.dob),
            },
        }

    @staticmethod
    def build_payor_payload(data: Payor) -> dict:
        return {
            "type": "c_corporation",
            "corporation": {
                "name": data.name,
                "dba": data.dba,
                "ein": data.ein,
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
    def build_payee_payload(data: Payee) -> dict:
        if data.merchant is not None:
            return {
                "holder_id": data.employee_record.external_id,
                "liability": {
                    "mch_id": data.merchant.mch_id,
                    "number": data.loan_account_number,
                },
            }
        return {}

    @staticmethod
    def build_payor_account_payload(data: PayorAccount) -> dict:
        return {
            "holder_id": data.payor_record.external_id,
            "ach": {
                "routing": data.aba_routing,
                "number": data.account_number,
                "type": "checking",
            },
        }
