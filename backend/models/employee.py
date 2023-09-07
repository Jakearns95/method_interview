import time
import uuid
from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    branch_id: str = Field(
        description="UUID for the branch the employee belongs to",
        example="BRC-5a32e859-e91a-490c-b4f2-bce67695f30c",
    )
    first_name: str = Field(
        description="First name of the employee",
        example="Larry",
    )
    last_name: str = Field(
        description="Last name of the employee",
        example="David",
    )
    dob: str = Field(
        description="Date of birth, in format YYYY-MM-DD, or Unix timestamp",
        example="1999-12-31",
    )
    phone: str = Field(
        description="Phone number of the employee",
        example="+16473020450",
    )
    status: str = Field(
        description="Status of the ",
        example="Pending",
    )
    external_id = Field(
        description="External id for the entity",
        example="ext_123456789",
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
