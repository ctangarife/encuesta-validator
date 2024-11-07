from app import db_pgl as db
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base_model import Base


class Survey(Base):
    __tablename__ = "survey"
    __table_args__ = {"schema": "administrator"}

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    # Relations
    questions = relationship("Question", back_populates="survey")
    responses = relationship("Response", back_populates="survey")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
