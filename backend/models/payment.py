import time
import uuid
from pydantic import BaseModel, Field


class Payment(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    employee_id: str = Field(
        description="The id of the employee who received a payment",
        example="5a32e859-e91a-490c-b4f2-bce67695f30c",
    )
    payor_id: str = Field(
        description="The id of the entity that made the payment",
        example="5a32e859-e91a-490c-b4f2-bce67695f30c",
    )
    payee_id: str = Field(
        description="The id of the employees liability account",
        example="5a32e859-e91a-490c-b4f2-bce67695f30c",
    )
    amount: str = Field(
        description="Amount to be paid in dollars",
        example="$7.03",
    )
    # TODO: can add pydantic statictyping
    status: str = Field(
        description="Status of the payment with method",
        example="Pending",
    )

    metadata: dict = Field(
        description="Metadata from method about the payment",
        example={
            "id": "pmt_rPrDPEwyCVUcm",
            "reversal_id": None,
            "source_trace_id": None,
            "destination_trace_id": None,
            "source": "acc_JMJZT6r7iHi8e",
            "destination": "acc_AXthnzpBnxxWP",
            "amount": 5000,
            "description": "Loan Pmt",
            "status": "pending",
            "error": None,
            "metadata": None,
            "estimated_completion_date": "2020-12-11",
            "source_settlement_date": "2020-12-09",
            "destination_settlement_date": "2020-12-11",
            "fee": None,
            "created_at": "2020-12-09T00:42:31.209Z",
            "updated_at": "2020-12-09T00:43:30.996Z",
        },
    )

    # TODO: can add in a mixin to set this for all models
    created_at = Field(
        description="When the person was registered (Unix timestamp)",
        default_factory=time.time(),
    )
    updated_at = Field(
        description="When the person was updated for the last time (Unix timestamp)",
        default_factory=time.time(),
    )
