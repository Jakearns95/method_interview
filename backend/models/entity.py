import time
import uuid
from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    corp_id: str = Field(
        description="UUID for the corporation the entity belongs to",
        example="CORP-e4025d0e-0491-49ef-8284-2738c2d0a0cf",
    )
    first_name: str = Field(
        description="First name of the employee",
        example="Larry",
    )
    address: dict = Field(
        description="Address of the entity",
        example={
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
        },
    )
    ein = Field(
        description="Employer Identification Number",
        example="123456789",
    )
    dba = Field(
        description="Doing Business As",
        example="Method",
    )
    account_id = Field(
        description="Institution for payments account id",
        example="acc_AXthnzpBnxxWP",
    )
    external_id = Field(
        description="External id for the entity",
        example="ext_123456789",
    )
    status: str = Field(
        description="Status of the ",
        example="Pending",
    )

    # TODO: can add in a mixin to set this for all models
    created_at = Field(
        alias="created",
        description="When the person was registered (Unix timestamp)",
        default_factory=time.time(),
    )
    updated_at = Field(
        alias="updated",
        description="When the person was updated for the last time (Unix timestamp)",
        default_factory=time.time(),
    )

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "branch_id": "BRC-5a32e859-e91a-490c-b4f2-bce67695f30c",
                "first_name": "Larry",
                "last_name": "David",
                "dob": "1999-12-31",
                "phone": "+16473020450",
            }
        }
