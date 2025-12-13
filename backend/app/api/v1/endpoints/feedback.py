from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Feedback as FeedbackModel
from app.schemas.feedback import Feedback as FeedbackSchema, FeedbackCreate

router = APIRouter()

@router.post("/", response_model=FeedbackSchema, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_in: FeedbackCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new feedback.
    """
    # Create a new SQLAlchemy model instance from the Pydantic schema
    db_feedback = FeedbackModel(**feedback_in.model_dump())
    
    # Add to the session and commit
    db.add(db_feedback)
    await db.commit()
    
    # Refresh the instance to get the data from the database (like id, created_at)
    await db.refresh(db_feedback)
    
    return db_feedback
