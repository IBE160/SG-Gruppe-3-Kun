from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_rate_limiting_enforcement():
    """
    Test AC 5.1.1: Requests exceeding the limit (e.g., 60/min) must be rejected with HTTP status 429.
    Test AC 5.1.2: Responses should include standard rate limit headers.
    """
    # Note: State is shared in memory limiter. We need to be careful with other tests running in parallel
    # or previous tests consuming the limit. 
    # Since we use a fresh TestClient, remote address might be consistent.
    
    # Hit the endpoint enough times to trigger the limit (60/min)
    limit = 60
    responses = []
    
    # We go a bit over to ensure we hit it
    for i in range(limit + 5):
        response = client.get("/health")
        responses.append(response)
        if response.status_code == 429:
            break
            
    # Check if we got a 429
    status_codes = [r.status_code for r in responses]
    
    # Ideally we should hit 429. 
    # However, if the limit is per minute and this runs in milliseconds, it will definitely hit it.
    assert 429 in status_codes, f"Did not trigger rate limit after {len(responses)} requests. Codes: {status_codes}"
    
    # Verify headers on a successful request
    ok_response = responses[0]
    assert ok_response.status_code == 200
    assert "X-RateLimit-Limit" in ok_response.headers
    assert "X-RateLimit-Remaining" in ok_response.headers
    assert "X-RateLimit-Reset" in ok_response.headers
    
    # Verify headers on 429 response
    blocked_response = responses[-1]
    assert blocked_response.status_code == 429
    assert "Retry-After" in blocked_response.headers
