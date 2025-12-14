import logging
from pythonjsonlogger.jsonlogger import JsonFormatter
from app.core.config import settings
from app.middleware.correlation_id import add_correlation_id_filter # Import the function

class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, message_dict, record_obj): # Corrected signature
        super().add_fields(log_record, message_dict, record_obj) # Call parent's add_fields with correct args
        # Add correlation_id if it exists in the log_record (added by the filter)
        if hasattr(record_obj, 'correlation_id') and record_obj.correlation_id:
            message_dict['correlation_id'] = record_obj.correlation_id

def configure_logging():
    log_level = logging.getLevelName(settings.LOG_LEVEL.upper())
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Only add handlers if not already present, to avoid duplicates in reloads/tests
    if not root_logger.handlers:
        formatter = CustomJsonFormatter(
            '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    add_correlation_id_filter() # Call the function to add the filter
    
    logging.info(f"Logging configured with level: {settings.LOG_LEVEL} and JSON format.")