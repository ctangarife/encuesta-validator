from app import db_pgl as db
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base_model import Base
import enum


class TypeIdentification(enum.Enum):
    CC = "CC"
    TI = "TI"
    CE = "CE"
    PASSPORT = "PASSPORT"


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    type_identification = Column(
        Enum(TypeIdentification), default=TypeIdentification.CC, nullable=False
    )
    identification = Column(String(20), nullable=True)
    student_code = Column(String(100), nullable=True)

    # Relations
    responses = relationship("Response", back_populates="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
