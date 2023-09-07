import time
import uuid
from pydantic import BaseModel, Field


class Account(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    holder_id: str = Field(
        description="The external ID of the entity owns the account (e.g. the employee or entity)",
        example="ent_y1a9e1fbnJ1f3",
    )
    liability = Field(
        description="A dict containing the liability account information",
        example={"mch_id": "mch_2", "account_number": "1122334455"},
    )
    ach = Field(
        description="A dict containing the ACH account information",
        example={
            # TODO: can add encryption to these fields
            "routing_number": "123456789",
            "account_number": "123456789",
            "type": "checking",
        },
    )

    status = Field(
        description="Status of the account",
        example="Pending",
    )
    external_id = Field(
        description="External id for the account",
        example="acc_b9q2XVAnNFbp3",
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
