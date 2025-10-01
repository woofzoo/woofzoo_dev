"""
Trace ID middleware for request tracking.

This module provides middleware to generate and inject trace IDs into requests
for better request tracking and logging correlation.
"""

import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable to store trace ID for the current request
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")


class TraceIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate and inject trace IDs into requests.
    
    This middleware generates a unique trace ID for each request and stores it
    in a context variable that can be accessed throughout the request lifecycle.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and inject trace ID.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware/handler in the chain
            
        Returns:
            The HTTP response
        """
        # Generate a unique trace ID for this request
        trace_id = str(uuid.uuid4())
        
        # Store the trace ID in the context variable
        trace_id_var.set(trace_id)
        
        # Add trace ID to request state for easy access
        request.state.trace_id = trace_id
        
        # Process the request
        response = await call_next(request)
        
        # Add trace ID to response headers for client tracking
        response.headers["X-Trace-ID"] = trace_id
        
        return response


def get_trace_id() -> str:
    """
    Get the current trace ID from the context.
    
    Returns:
        The current trace ID, or empty string if not set
    """
    return trace_id_var.get()


def set_trace_id(trace_id: str) -> None:
    """
    Set the trace ID in the context.
    
    Args:
        trace_id: The trace ID to set
    """
    trace_id_var.set(trace_id)
