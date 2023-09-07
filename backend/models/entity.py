from utils.constants import EntityStatus
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Enum as saEnum  # Avoid conflicts with Python Enum
from sqlalchemy.types import String
from sqlalchemy_utils import UUIDType

from .base import Base, Timestamp, enum_values, hex_uuid


class Entity(Base, Timestamp):
    __tablename__ = "entities"

    id = Column(UUIDType, primary_key=True, index=True, default=hex_uuid)
    corp_id = Column(UUIDType(binary=False), unique=True)
    name = Column(String)
    address_id = Column(UUIDType(binary=False), ForeignKey("addresses.id"))
    ein = Column(String)
    dba = Column(String)
    external_entity_id = Column(UUIDType)
    status = Column(saEnum(EntityStatus, values_callable=enum_values), nullable=False)
