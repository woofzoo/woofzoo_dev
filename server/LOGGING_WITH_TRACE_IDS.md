# Logging with Trace IDs

This document explains how to use the enhanced logging system with trace IDs for better request tracking and debugging.

## Overview

The application now includes a comprehensive trace ID system that:
- Generates unique trace IDs for each request
- Automatically includes trace IDs in all log messages
- Provides context managers for background tasks
- Stores trace IDs in response headers for client tracking

## Features

### 1. Automatic Trace ID Generation
Every incoming HTTP request automatically gets a unique trace ID that follows the request through its entire lifecycle.

### 2. Enhanced Log Format
All log messages now include the trace ID in the format:
```
2024-01-15 10:30:45.123 | INFO     | [a1b2c3d4] | app.controllers.pet:create_pet:32 - Pet created successfully
```

**Note**: Each log message is properly formatted with line breaks to ensure readability. All standard library logging (including uvicorn) is automatically intercepted and redirected to use our consistent format.

**Traceback Filtering**: Exception tracebacks are automatically filtered to show only application code, hiding framework internals (SQLAlchemy, FastAPI, etc.) for cleaner, more focused debugging.

### 3. File Logging
- **General logs**: `logs/app.log` (rotating, 10MB, 14 days retention)
- **Error logs**: `logs/error.log` (rotating, 5MB, 30 days retention)

### 4. Request Logging
All HTTP requests and responses are automatically logged with trace IDs, including:
- Request method, path, and query parameters
- Response status code and processing time
- Client IP and user agent information

### 5. Context Managers
For background tasks or non-request contexts, use the provided context managers:

```python
from app.context.trace_context import trace_context, async_trace_context

# For synchronous code
with trace_context() as trace_id:
    logger.info("Processing background task")
    # All logs in this context will include the trace_id

# For asynchronous code
async with async_trace_context() as trace_id:
    logger.info("Processing async background task")
    # All logs in this context will include the trace_id
```

## Usage Examples

### In Controllers
```python
from loguru import logger

class PetController:
    def create_pet(self, pet_data: PetCreate) -> PetResponse:
        try:
            logger.info("Creating new pet", extra={"pet_name": pet_data.name, "pet_type": pet_data.pet_type})
            pet = self.pet_service.create_pet(pet_data)
            logger.info("Pet created successfully", extra={"pet_id": pet.id, "pet_name": pet.name})
            return PetResponse.model_validate(pet)
        except ValueError as e:
            logger.warning("Pet creation failed - validation error", extra={"error": str(e), "pet_name": pet_data.name})
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.exception("Pet creation failed - unexpected error", extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "pet_name": pet_data.name,
                "pet_type": pet_data.pet_type
            })
            raise HTTPException(status_code=500, detail="Failed to create pet")
```

### In Services
```python
from loguru import logger

class PetService:
    def create_pet(self, pet_data: PetCreate) -> Pet:
        logger.debug("Validating pet data")
        # ... validation logic ...
        
        logger.info("Saving pet to database", extra={"pet_name": pet_data.name})
        # ... database operations ...
        
        logger.info("Pet saved successfully", extra={"pet_id": pet.id})
        return pet
```

### In Background Tasks
```python
from app.context.trace_context import async_trace_context
from loguru import logger

async def process_pet_photos(pet_id: str):
    async with async_trace_context() as trace_id:
        logger.info("Starting photo processing", extra={"pet_id": pet_id})
        # ... processing logic ...
        logger.info("Photo processing completed", extra={"pet_id": pet_id})
```

## Log Levels

The system supports all standard log levels:
- `DEBUG`: Detailed information for debugging
- `INFO`: General information about application flow
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for handled exceptions
- `CRITICAL`: Critical errors that may cause the application to stop

## Trace ID Format

Trace IDs are UUID4 format (e.g., `a1b2c3d4-e5f6-7890-abcd-ef1234567890`), but in logs they're shortened to the first 8 characters for readability (e.g., `[a1b2c3d4]`).

## Response Headers

Every HTTP response includes the trace ID in the `X-Trace-ID` header, allowing clients to correlate requests with server logs.

## Configuration

The logging system is configured in `app/logger.py` and can be customized by modifying the `configure_logging()` function.

### Environment Variables
- `DEBUG`: Set to `true` to enable debug-level logging
- Log files are created in the `logs/` directory

## Best Practices

1. **Use structured logging**: Include relevant context in log messages using the `extra` parameter
2. **Log at appropriate levels**: Use DEBUG for detailed debugging, INFO for important flow events, WARNING for potential issues, ERROR for exceptions
3. **Include trace IDs in error reports**: When reporting errors to users, include the trace ID for easier debugging
4. **Use context managers for background tasks**: Always wrap background tasks with trace context managers

## Troubleshooting

### No Trace ID in Logs
If you see `[no-trace]` in logs, it means the code is running outside of a request context. Use the context managers for background tasks.

### Missing Log Files
Ensure the `logs/` directory exists and has proper write permissions.

### Performance Considerations
- Logging is asynchronous by default (`enqueue=True`)
- File rotation prevents log files from growing too large
- Consider log level in production (INFO vs DEBUG)
