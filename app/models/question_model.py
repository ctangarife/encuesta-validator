from app import db_pgl as db
from sqlalchemy import Column, String, Integer, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base_model import Base
import enum


class TypeQuestion(enum.Enum):
    Single = "Single"
    Multiple = "Multiple"
    Open = "Open"
    Scale = "Scale"
    Option = "Option"


class Question(Base):
    __tablename__ = "question"
    __table_args__ = {"schema": "administrator"}

    question = Column(String(200), nullable=False)
    type = Column(Enum(TypeQuestion), default=TypeQuestion.Single, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    is_required = Column(Boolean, default=False, nullable=False)
    order = Column(Integer, nullable=True)

    # Relations
    id_survey = Column(
        UUID, ForeignKey("administrator.survey.id"), nullable=False
    )
    survey = relationship("Survey", back_populates="questions")
    responses = relationship("Response", back_populates="question")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
