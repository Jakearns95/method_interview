from utils.constants import PaymentStatus
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Enum as saEnum  # Avoid conflicts with Python Enum
from sqlalchemy_utils import UUIDType
from sqlalchemy.types import BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from .base import Base, Timestamp, enum_values, hex_uuid


class Payment(Base, Timestamp):
    __tablename__ = "payments"

    id = Column(UUIDType, primary_key=True, index=True, default=hex_uuid)
    employee_id = Column(UUIDType(binary=False), ForeignKey("employees.id"))
    amount = Column(BigInteger)
    payment_data = Column(MutableDict.as_mutable(JSONB))
    payee_id = Column(UUIDType(binary=False), ForeignKey("liabilities.id"))
    payor_id = Column(UUIDType(binary=False), ForeignKey("entities.id"))
    status = Column(saEnum(PaymentStatus, values_callable=enum_values))
