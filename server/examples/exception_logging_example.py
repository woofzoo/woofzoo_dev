#!/usr/bin/env python3
"""
Example showing proper exception logging with trace IDs.

This example demonstrates how to use logger.exception() correctly
to get full tracebacks with trace ID correlation.
"""

import sys
import os
import uuid

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Mock the trace_id module for testing
class MockTraceID:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())
    
    def get_trace_id(self):
        return self.trace_id

# Mock the trace_id module
sys.modules['app.middleware.trace_id'] = MockTraceID()

from app.logger import configure_logging
from loguru import logger

def simulate_pet_creation():
    """Simulate pet creation with proper exception logging."""
    logger.info("Starting pet creation process", extra={"operation": "create_pet"})
    
    try:
        # Simulate some validation
        pet_name = "Buddy"
        pet_age = -5  # This will cause a validation error
        
        if pet_age < 0:
            raise ValueError("Pet age cannot be negative")
        
        # Simulate database operation
        raise ConnectionError("Database connection failed")
        
    except ValueError as e:
        logger.warning("Pet creation failed - validation error", extra={
            "error": str(e),
            "pet_name": pet_name,
            "pet_age": pet_age
        })
        raise
        
    except Exception as e:
        logger.exception("Pet creation failed - unexpected error", extra={
            "error": str(e),
            "error_type": type(e).__name__,
            "pet_name": pet_name,
            "pet_age": pet_age
        })
        raise

def simulate_nested_exception():
    """Simulate a nested exception scenario."""
    def database_operation():
        raise ConnectionError("Connection timeout")
    
    def business_logic():
        try:
            database_operation()
        except ConnectionError as e:
            logger.exception("Database operation failed", extra={
                "operation": "database_query",
                "error": str(e)
            })
            raise
    
    try:
        business_logic()
    except Exception as e:
        logger.exception("Business logic failed", extra={
            "operation": "process_data",
            "error": str(e)
        })

def main():
    """Run the exception logging examples."""
    print("Exception Logging with Trace IDs Example")
    print("=" * 50)
    
    # Configure logging
    configure_logging(debug=True)
    
    # Example 1: Validation error
    print("\n1. Validation Error Example:")
    print("-" * 30)
    try:
        simulate_pet_creation()
    except ValueError:
        pass  # Expected error
    
    # Example 2: Nested exception
    print("\n2. Nested Exception Example:")
    print("-" * 30)
    simulate_nested_exception()
    
    print("\n" + "=" * 50)
    print("Examples completed. Notice how logger.exception() shows:")
    print("- Full traceback with line numbers")
    print("- Trace ID correlation")
    print("- Structured context data")

if __name__ == "__main__":
    main()
