import os
import uuid

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime

Base = declarative_base()
metadata = Base.metadata

enum_values = lambda x: [e.value for e in x]

load_dotenv(find_dotenv(".env.localdev"))
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI").replace(
    "postgres://", "postgresql://", 1
)


def hex_uuid():
    return uuid.uuid4().hex


@declarative_mixin
class Timestamp:
    created_at: DateTime = Column(DateTime, default=func.now())
    updated_at: DateTime = Column(DateTime, default=func.now(), onupdate=func.now())
