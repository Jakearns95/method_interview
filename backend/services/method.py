class MethodService:
    @classmethod
    def create_entity(cls, payload: dict):
        """This will create the entity for both individuals and corporations"""
        return {"status": "active", "id": 1}

    @classmethod
    def create_account(cls, payload: dict):
        """This will create the bank and liability accounts for both debits and credits"""
        return {"status": "active", "id": 1}

    @classmethod
    def create_payment(cls):
        """This will initiate the payments"""
        pass

    @classmethod
    def get_merchant(cls):
        """This will retrieve all the merchants in methods db"""

        # TODO get and save these - update the document record if anything changes
        # use my internal record for each plaid account to get merchant id instead of api calls
        pass

    @staticmethod
    def process_payment(payment: dict) -> dict:
        # Logic to call the third-party API with the payment data
        # Replace this with your actual API call logic
        response = {
            "id": "some_id_based_on_payment",
            "status": "processed",
            "payload": "payload_for_this_payment",
        }
        return response
