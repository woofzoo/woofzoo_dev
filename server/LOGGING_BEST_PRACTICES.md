# Logging Best Practices with Trace IDs

This document outlines the best practices for logging in the WoofZoo application with trace ID support.

## Exception Logging

### ❌ **Don't Do This:**
```python
except Exception as e:
    logger.exception("Failed to create pet")
    # This doesn't provide enough context
```

### ✅ **Do This Instead:**
```python
except Exception as e:
    logger.exception("Pet creation failed - unexpected error", extra={
        "error": str(e),
        "error_type": type(e).__name__,
        "pet_name": pet_data.name,
        "pet_type": pet_data.pet_type
    })
```

## Structured Logging Guidelines

### 1. **Always Include Context**
```python
# Good
logger.info("User login successful", extra={
    "user_id": user.id,
    "email": user.email,
    "login_method": "password"
})

# Bad
logger.info("User logged in")
```

### 2. **Use Appropriate Log Levels**
- **DEBUG**: Detailed information for debugging (variable values, step-by-step process)
- **INFO**: Important business events (user actions, successful operations)
- **WARNING**: Potential issues that don't stop execution (deprecated API usage, validation warnings)
- **ERROR**: Errors that are handled but indicate problems (validation failures, external service errors)
- **CRITICAL**: Serious errors that may cause the application to stop

### 3. **Exception Handling Pattern**
```python
def create_resource(self, data: ResourceCreate) -> ResourceResponse:
    try:
        logger.info("Creating resource", extra={"resource_type": data.type})
        resource = self.service.create_resource(data)
        logger.info("Resource created successfully", extra={"resource_id": resource.id})
        return ResourceResponse.model_validate(resource)
        
    except ValueError as e:
        logger.warning("Resource creation failed - validation error", extra={
            "error": str(e),
            "resource_type": data.type
        })
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except Exception as e:
        logger.error("Resource creation failed - unexpected error", extra={
            "error": str(e),
            "error_type": type(e).__name__,
            "resource_type": data.type
        })
        logger.exception("Full exception details for resource creation failure")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create resource"
        )
```

### 4. **Request Lifecycle Logging**
```python
# At the start of a request handler
logger.info("Request started", extra={
    "method": request.method,
    "path": request.url.path,
    "user_id": getattr(request.state, 'user_id', None)
})

# During processing
logger.debug("Processing step 1", extra={"step": "validation"})
logger.debug("Processing step 2", extra={"step": "database_save"})

# At the end
logger.info("Request completed successfully", extra={
    "status_code": 200,
    "processing_time": 0.123
})
```

### 5. **Database Operations**
```python
logger.info("Executing database query", extra={
    "query_type": "SELECT",
    "table": "users",
    "filters": {"status": "active"}
})

logger.debug("Query parameters", extra={"params": query_params})
```

### 6. **External Service Calls**
```python
logger.info("Calling external service", extra={
    "service": "payment_gateway",
    "endpoint": "/api/charge",
    "amount": 100.00
})

try:
    response = external_service.charge(amount)
    logger.info("External service call successful", extra={
        "service": "payment_gateway",
        "transaction_id": response.transaction_id
    })
except Exception as e:
    logger.error("External service call failed", extra={
        "service": "payment_gateway",
        "error": str(e),
        "error_type": type(e).__name__
    })
    logger.exception("Full exception details for external service failure")
```

## Common Patterns

### 1. **Before/After Operations**
```python
logger.info("Starting operation", extra={"operation": "user_registration"})
# ... operation code ...
logger.info("Operation completed", extra={"operation": "user_registration", "result": "success"})
```

### 2. **Conditional Logging**
```python
if user.is_premium:
    logger.info("Premium user action", extra={"user_id": user.id, "action": "premium_feature"})
```

### 3. **Performance Logging**
```python
import time

start_time = time.time()
# ... operation ...
processing_time = time.time() - start_time
logger.info("Operation completed", extra={"processing_time": processing_time})
```

### 4. **Security Events**
```python
logger.warning("Suspicious activity detected", extra={
    "user_id": user.id,
    "ip_address": request.client.host,
    "activity": "multiple_failed_logins",
    "attempts": 5
})
```

## What Gets Logged

With our current setup, every log message includes:
- **Timestamp**: Precise time with milliseconds
- **Log Level**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Trace ID**: 8-character trace ID for request correlation
- **Location**: File, function, and line number
- **Message**: The actual log message
- **Exception Traceback**: Filtered stack trace showing only application code (when using `logger.exception()`)

## Traceback Filtering

Our logging system automatically filters exception tracebacks to show only relevant application code:

### ✅ **What You'll See:**
```
File "/app/controllers/pet.py", line 33, in create_pet
    pet = self.pet_service.create_pet(pet_data)
File "/app/services/pet.py", line 41, in create_pet
    pet = self.pet_repository.create(pet_data)
File "/app/repositories/pet.py", line 25, in create
    self.session.commit()
ValueError: Foreign key constraint violation
```

### ❌ **What You Won't See:**
- SQLAlchemy internal calls
- FastAPI framework code
- Python standard library internals
- Third-party package internals

## Testing Your Logging

Use the test script to verify your logging works correctly:
```bash
python test_exception_logging.py
```

## File Locations

- **Console**: All logs go to stderr with trace IDs
- **General Logs**: `logs/app.log` (rotating, 10MB, 14 days)
- **Error Logs**: `logs/error.log` (rotating, 5MB, 30 days)

## Debugging Tips

1. **Search by Trace ID**: Use the trace ID to follow a complete request flow
2. **Check Error Logs**: Look in `logs/error.log` for all error-level messages
3. **Use Extra Data**: Include relevant context in the `extra` parameter
4. **Exception Details**: Always use `logger.exception()` for unexpected errors to get full tracebacks
