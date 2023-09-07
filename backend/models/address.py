from sqlalchemy.types import String
from sqlalchemy.schema import Column
from sqlalchemy_utils import UUIDType

from .base import Base, Timestamp, hex_uuid


class Address(Base, Timestamp):
    __tablename__ = "addresses"

    id = Column(UUIDType, primary_key=True, index=True, default=hex_uuid)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
