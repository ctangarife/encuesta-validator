from app import db_pgl as db
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base_model import Base


class Response(Base):
    __tablename__ = "response"
    __table_args__ = {"schema": "public"}

    id_user = Column(UUID(as_uuid=True), ForeignKey("public.user.id"), nullable=False)
    id_survey = Column(
        UUID(as_uuid=True), ForeignKey("administrator.survey.id"), nullable=False
    )
    id_question = Column(
        UUID(as_uuid=True), ForeignKey("administrator.question.id"), nullable=False
    )

    response = Column(String(255), nullable=True)
    valid = Column(Boolean, default=True, nullable=False)

    # Relations
    user = relationship("User", back_populates="responses")
    survey = relationship("Survey", back_populates="responses")
    question = relationship("Question", back_populates="responses")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
