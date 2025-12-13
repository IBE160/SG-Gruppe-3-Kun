from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(String, index=True)
    message_id = Column(String, index=True)
    rating = Column(String, nullable=False)
    user_id = Column(String, index=True, nullable=True)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
