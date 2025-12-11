from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()

@router.get("/db-check")
async def health_check_db(db: AsyncSession = Depends(get_db)):
    """
    Check database connectivity by executing a simple query.
    """
    try:
        # Execute a simple query using text()
        result = await db.execute(text("SELECT 1"))
        # Fetch the result to ensure execution happened
        value = result.scalar() 
        return {"status": "ok", "db_response": value}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
