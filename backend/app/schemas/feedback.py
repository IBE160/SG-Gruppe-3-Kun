from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    """Base model for feedback, containing common fields."""
    chat_session_id: str
    message_id: str
    rating: str  # e.g., "thumbs_up", "thumbs_down"
    user_id: Optional[str] = None
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    """
    Schema for creating new feedback. Inherits all fields from FeedbackBase.
    This is the expected model for POST requests.
    """
    pass

class Feedback(FeedbackBase):
    """
    Schema for representing feedback data, including DB-generated fields.
    This is the model for GET responses.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
