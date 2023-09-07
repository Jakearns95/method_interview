from utils.constants import AccountStatus
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Enum as saEnum  # Avoid conflicts with Python Enum
from sqlalchemy.types import String
from sqlalchemy_utils import UUIDType

from .base import Base, Timestamp, enum_values, hex_uuid


class BankAccount(Base, Timestamp):
    __tablename__ = "bank_accounts"

    id = Column(UUIDType, primary_key=True, index=True, default=hex_uuid)
    entity_id = Column(UUIDType(binary=False), ForeignKey("entities.id"))
    account_number = Column(String)
    routing_number = Column(String)
    status = Column(saEnum(AccountStatus, values_callable=enum_values))
