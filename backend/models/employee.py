from utils.constants import EntityStatus
from sqlalchemy.schema import Column
from sqlalchemy.types import Enum as saEnum  # Avoid conflicts with Python Enum
from sqlalchemy.types import String
from sqlalchemy_utils import UUIDType

from .base import Base, Timestamp, enum_values, hex_uuid


class Employee(Base, Timestamp):
    __tablename__ = "employees"

    id = Column(UUIDType, primary_key=True, index=True, default=hex_uuid)
    employee_id = Column(UUIDType(binary=False), unique=True)
    branch_id = Column(
        UUIDType(binary=False),
    )
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(String)
    phone = Column(String)
    status = Column(saEnum(EntityStatus, values_callable=enum_values))
    external_entity_id = Column(UUIDType)
