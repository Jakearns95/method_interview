from typing import Any, Dict, Optional

from pydantic import BaseModel


class BatchFile(BaseModel):
    content: Dict[str, Any]


class Employee(BaseModel):
    dunkin_id: str
    dunkin_branch: str
    first_name: str
    last_name: str
    dob: str
    phone_number: str
    external_status: Optional[str]
    external_id: Optional[str]


class Address(BaseModel):
    line1: str
    city: str
    state: str
    zip: str
    external_status: Optional[str]
    external_id: Optional[str]


class Payor(BaseModel):
    dunkin_id: str
    name: str
    dba: str
    ein: str
    address: Address
    external_status: Optional[str]
    external_id: Optional[str]


class PayorAccount(BaseModel):
    aba_routing: str
    account_number: str
    payor_record: Payor  # The MongoDB ObjectId of the associated Payor
    external_status: Optional[str]
    external_id: Optional[str]


class Payee(BaseModel):
    plaid_id: str
    loan_account_number: str
    merchant: Optional[object]
    employee_record: Optional[Employee]
    external_status: Optional[str]
    external_id: Optional[str]


class Payment(BaseModel):
    employee: Employee
    payor_account: PayorAccount
    payee: Payee
    amount_cents: int
    external_status: Optional[str]
    external_id: Optional[str]
