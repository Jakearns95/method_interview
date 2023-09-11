from pydantic import BaseModel
from typing import Any, Dict, Optional


class BatchFile(BaseModel):
    content: Dict[str, Any]


class Employee(BaseModel):
    dunkin_id: str
    dunkin_branch: str
    first_name: str
    last_name: str
    dob: str
    phone_number: str


class Address(BaseModel):
    line1: str
    city: str
    state: str
    zip: str


class Payor(BaseModel):
    dunkin_id: str
    name: str
    dba: str
    ein: str
    address: Address


class PayorAccount(BaseModel):
    aba_routing: str
    account_number: str
    payor_id: object  # The MongoDB ObjectId of the associated Payor


class Payee(BaseModel):
    plaid_id: str
    loan_account_number: str


class Payment(BaseModel):
    employee: Employee
    payor_account: PayorAccount
    payee: Payee
    amount: float
