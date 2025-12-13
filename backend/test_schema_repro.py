
import asyncio
import json
from app.schemas.chat import ChatRequest, UserRole

async def test_schema():
    print("Testing Schema Validation...")
    
    # Test 1: Project Manager / Admin
    try:
        payload = {"message": "test", "user_role": "Project Manager / Admin"}
        request = ChatRequest(**payload)
        print(f"✅ Success: {request.user_role}")
    except Exception as e:
        print(f"❌ Failed 'Project Manager / Admin': {e}")

    # Test 2: Construction Worker
    try:
        payload = {"message": "test", "user_role": "Construction Worker"}
        request = ChatRequest(**payload)
        print(f"✅ Success: {request.user_role}")
    except Exception as e:
        print(f"❌ Failed 'Construction Worker': {e}")

    # Test 3: Supplier / Subcontractor
    try:
        payload = {"message": "test", "user_role": "Supplier / Subcontractor"}
        request = ChatRequest(**payload)
        print(f"✅ Success: {request.user_role}")
    except Exception as e:
        print(f"❌ Failed 'Supplier / Subcontractor': {e}")

if __name__ == "__main__":
    asyncio.run(test_schema())
