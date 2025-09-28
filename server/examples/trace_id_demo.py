#!/usr/bin/env python3
"""
Demo script to showcase trace ID logging functionality.

This script demonstrates how trace IDs work in different contexts:
1. Request context (simulated)
2. Background task context
3. Nested context scenarios
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.logger import configure_logging
from app.context.trace_context import trace_context, async_trace_context
from loguru import logger


def simulate_request_context():
    """Simulate a request context with trace ID."""
    print("=== Simulating Request Context ===")
    
    # This would normally be done by the TraceIDMiddleware
    from app.middleware.trace_id import set_trace_id
    import uuid
    
    trace_id = str(uuid.uuid4())
    set_trace_id(trace_id)
    
    logger.info("Request started")
    logger.info("Processing user data", extra={"user_id": "12345"})
    logger.warning("Deprecated API endpoint used", extra={"endpoint": "/api/v1/old"})
    logger.info("Request completed successfully")
    
    print(f"Trace ID used: {trace_id}")
    print()


def simulate_background_task():
    """Simulate a background task with trace context."""
    print("=== Simulating Background Task ===")
    
    with trace_context() as trace_id:
        logger.info("Background task started")
        logger.info("Processing batch data", extra={"batch_size": 100})
        logger.info("Sending notifications", extra={"recipients": 50})
        logger.info("Background task completed")
        
        print(f"Trace ID used: {trace_id}")
    print()


async def simulate_async_background_task():
    """Simulate an async background task with trace context."""
    print("=== Simulating Async Background Task ===")
    
    async with async_trace_context() as trace_id:
        logger.info("Async background task started")
        logger.info("Fetching external data", extra={"api": "external-service"})
        await asyncio.sleep(0.1)  # Simulate async work
        logger.info("Processing external data")
        logger.info("Async background task completed")
        
        print(f"Trace ID used: {trace_id}")
    print()


def simulate_nested_contexts():
    """Simulate nested trace contexts."""
    print("=== Simulating Nested Contexts ===")
    
    with trace_context() as outer_trace_id:
        logger.info("Outer context started")
        
        with trace_context() as inner_trace_id:
            logger.info("Inner context started")
            logger.info("Processing inner task")
            logger.info("Inner context completed")
        
        logger.info("Outer context continuing")
        logger.info("Outer context completed")
        
        print(f"Outer Trace ID: {outer_trace_id}")
        print(f"Inner Trace ID: {inner_trace_id}")
    print()


def simulate_error_scenario():
    """Simulate error logging with trace ID."""
    print("=== Simulating Error Scenario ===")
    
    with trace_context() as trace_id:
        logger.info("Starting operation that will fail")
        
        try:
            # Simulate an error
            result = 1 / 0
        except ZeroDivisionError as e:
            logger.error("Division by zero error occurred", extra={"operation": "division"})
            logger.exception("Full exception details")
        
        logger.info("Error handling completed")
        print(f"Trace ID used: {trace_id}")
    print()


async def main():
    """Run all demo scenarios."""
    print("Trace ID Logging Demo")
    print("=" * 50)
    print()
    
    # Configure logging
    configure_logging(debug=True)
    
    # Run synchronous demos
    simulate_request_context()
    simulate_background_task()
    simulate_nested_contexts()
    simulate_error_scenario()
    
    # Run async demo
    await simulate_async_background_task()
    
    print("Demo completed! Check the logs/ directory for log files.")
    print("Notice how each log entry includes a trace ID in brackets.")


if __name__ == "__main__":
    asyncio.run(main())
