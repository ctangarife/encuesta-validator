from app import db_pgl as db
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
import uuid


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)
    deleted = Column(Boolean, default=False, nullable=False)
    created_by = Column(String(30), nullable=True)
    updated_by = Column(String(30), nullable=True)
    deleted_by = Column(String(30), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
