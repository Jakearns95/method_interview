from utils.constants import AccountStatus
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Enum as saEnum  # Avoid conflicts with Python Enum
from sqlalchemy.types import String
from sqlalchemy_utils import UUIDType

from .base import Base, Timestamp, enum_values, hex_uuid


class Liability(Base, Timestamp):
    __tablename__ = "liabilities"

    id = Column(UUIDType, primary_key=True, index=True, default=hex_uuid)
    entity_id = Column(UUIDType(binary=False), ForeignKey("entities.id"))
    mch_id = Column(String)
    account_number = Column(String)
    status = Column(saEnum(AccountStatus, values_callable=enum_values))
