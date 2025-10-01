"""
Trace context manager for request tracking.

This module provides context managers and utilities for handling trace IDs
in different contexts (requests, background tasks, etc.).
"""

import uuid
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator, Optional

from app.middleware.trace_id import get_trace_id, set_trace_id


@contextmanager
def trace_context(trace_id: Optional[str] = None) -> Generator[str, None, None]:
    """
    Context manager for setting a trace ID in the current context.
    
    Args:
        trace_id: Optional trace ID to use. If not provided, generates a new one.
        
    Yields:
        The trace ID being used in this context
    """
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    
    # Store the original trace ID
    original_trace_id = get_trace_id()
    
    try:
        # Set the new trace ID
        set_trace_id(trace_id)
        yield trace_id
    finally:
        # Restore the original trace ID
        set_trace_id(original_trace_id)


@asynccontextmanager
async def async_trace_context(trace_id: Optional[str] = None) -> AsyncGenerator[str, None]:
    """
    Async context manager for setting a trace ID in the current context.
    
    Args:
        trace_id: Optional trace ID to use. If not provided, generates a new one.
        
    Yields:
        The trace ID being used in this context
    """
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    
    # Store the original trace ID
    original_trace_id = get_trace_id()
    
    try:
        # Set the new trace ID
        set_trace_id(trace_id)
        yield trace_id
    finally:
        # Restore the original trace ID
        set_trace_id(original_trace_id)


def generate_trace_id() -> str:
    """
    Generate a new trace ID.
    
    Returns:
        A new UUID4-based trace ID
    """
    return str(uuid.uuid4())


def get_current_trace_id() -> str:
    """
    Get the current trace ID from the context.
    
    Returns:
        The current trace ID, or empty string if not set
    """
    return get_trace_id()