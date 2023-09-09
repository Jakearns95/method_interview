from pydantic import BaseModel
from typing import Any, Dict


class BatchFile(BaseModel):
    content: Dict[str, Any]


class Employee(BaseModel):
    DunkinId: str
    DunkinBranch: str
    FirstName: str
    LastName: str
    DOB: str
    PhoneNumber: str


class Address(BaseModel):
    Line1: str
    City: str
    State: str
    Zip: str


class Payor(BaseModel):
    DunkinId: str
    ABARouting: str
    AccountNumber: str
    Name: str
    DBA: str
    EIN: str
    Address: Address


class Payee(BaseModel):
    PlaidId: str
    LoanAccountNumber: str


class Payment(BaseModel):
    employee: Employee
    payor: Payor
    payee: Payee
    amount: float
