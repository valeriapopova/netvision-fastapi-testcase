import uuid

from sqlalchemy import Column, UUID, String
from sqlalchemy.orm.decl_api import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Entry_DB(Base):
    __tablename__ = "entries"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    text = Column(String, nullable=False)
