import json
import logging
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.logging import configure_logging, CustomJsonFormatter
from app.middleware.correlation_id import correlation_id_ctx
import pytest

# Ensure logging is configured for tests
@pytest.fixture(autouse=True)
def setup_logging_for_test(caplog):
    # Ensure caplog captures all levels
    caplog.set_level(logging.INFO)
    yield

client = TestClient(app)

def get_json_log_records(caplog_records):
    """Helper to extract JSON log records formatted by CustomJsonFormatter."""
    json_records = []
    # Instantiate formatter once for consistent formatting
    formatter = CustomJsonFormatter(
        '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
    )
    for record in caplog_records:
        try:
            # Check if the record is already a structured JSON log (e.g., from logfire)
            if hasattr(record, 'correlation_id'): # Check for correlation ID from our filter
                # If correlation_id is present, it means our filter has run on this record
                # We can then format it explicitly
                formatted_message = formatter.format(record)
                json_records.append(json.loads(formatted_message))
            elif record.message.startswith('{') and record.message.endswith('}'):
                # Attempt to parse messages that look like JSON (e.g., from logfire)
                json_records.append(json.loads(record.message))
            else:
                # Fallback to formatting non-structured messages
                formatted_message = formatter.format(record)
                json_records.append(json.loads(formatted_message))
        except (json.JSONDecodeError, AttributeError):
            # Skip non-JSON or improperly formatted logs
            continue
    return json_records

def test_json_logging_format(caplog):
    """
    Test AC 5.3.1: Backend logs must be output in valid JSON format.
    """
    client.get("/health")
    json_logs = get_json_log_records(caplog.records)
    
    assert len(json_logs) > 0, "No JSON logs captured"
    # Find a log entry that is definitely from our application and is JSON
    app_log_found = False
    for log in json_logs:
        if log.get("message") and "Logging configured with level" in log["message"] and "INFO" in log["levelname"]:
            app_log_found = True
            break
    assert app_log_found, "Did not find expected application setup log"

def test_log_content_http_request(caplog):
    """
    Test AC 5.3.2: Logs must capture HTTP method, path, status, time, and Correlation ID.
    """
    response = client.get("/health")
    assert response.status_code == 200
    
    json_logs = get_json_log_records(caplog.records)
    
    # Find the log record corresponding to the request/response, preferably from logfire's HTTP instrumentation
    http_log_record = next((log for log in json_logs if log.get("message") and "GET /health" in log["message"] and log.get("correlation_id")), None)
    
    assert http_log_record is not None, f"Did not find a relevant HTTP request log with Correlation ID. All logs: {json_logs}"
    
    assert "levelname" in http_log_record
    assert "asctime" in http_log_record
    assert "message" in http_log_record
    assert "correlation_id" in http_log_record
    assert http_log_record["correlation_id"] is not None
    
    assert "GET /health" in http_log_record["message"]
    assert "status_code" in http_log_record # Logfire usually adds this as a field

def test_log_content_correlation_id_propagation(caplog):
    """
    Test AC 5.3.2: Verify Correlation ID is generated and returned in headers and logs.
    """
    response = client.get("/health")
    
    assert "X-Correlation-ID" in response.headers
    response_correlation_id = response.headers["X-Correlation-ID"]
    
    json_logs = get_json_log_records(caplog.records)
    
    logged_correlation_id = None
    for parsed_log in json_logs:
        if parsed_log.get("correlation_id") == response_correlation_id:
            logged_correlation_id = parsed_log["correlation_id"]
            break
    
    assert logged_correlation_id == response_correlation_id, f"Correlation ID {response_correlation_id} not propagated to logs. All logs: {json_logs}"

def test_unhandled_exception_logging(caplog):
    """
    Test AC 5.3.3: Uncaught exceptions and 500 errors must be logged with a full stack trace.
    """
    class TestException(Exception):
        pass

    @app.get("/test-error-route-for-logging-test") # Changed route name to avoid conflict
    async def test_error_route():
        raise TestException("This is a test error")

    response = client.get("/test-error-route-for-logging-test")
    
    assert response.status_code == 500
    
    json_logs = get_json_log_records(caplog.records)
    
    exception_log_record = None
    for parsed_log in json_logs:
        if parsed_log.get("levelname") == "ERROR" and "test-error" in parsed_log.get("message", ""):
            exception_log_record = parsed_log
            break
    
    assert exception_log_record is not None, f"Did not find the unhandled exception log. All logs: {json_logs}"
    assert "exc_info" in exception_log_record or "exc_text" in exception_log_record
    assert "TestException: This is a test error" in exception_log_record.get("exc_info", "") or \
           "TestException: This is a test error" in exception_log_record.get("message", "")
    assert "Traceback (most recent call last)" in exception_log_record.get("exc_info", "")