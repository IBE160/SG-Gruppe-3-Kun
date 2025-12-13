import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_feedback_table_created(test_db: AsyncSession):
    """
    Tests if the 'feedback' table is successfully created in the test database.
    """
    # The 'test_db' fixture handles the setup and teardown of the DB
    # We just need to inspect it here.
    
    def check_table(conn):
        inspector = inspect(conn)
        return inspector.has_table("feedback")

    async with test_db.bind.begin() as conn:
        has_table = await conn.run_sync(check_table)

    assert has_table, "The 'feedback' table should exist in the database after initialization."
