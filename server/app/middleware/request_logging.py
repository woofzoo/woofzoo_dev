"""
Request logging middleware for access logs with trace IDs.

This module provides middleware to log HTTP requests and responses
with trace ID correlation.
"""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log HTTP requests and responses with trace IDs.
    
    This middleware logs request details including method, path, status code,
    and response time, all correlated with the trace ID.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log access details.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware/handler in the chain
            
        Returns:
            The HTTP response
        """
        # Get trace ID from request state
        trace_id = getattr(request.state, 'trace_id', 'no-trace')
        
        # Start timing
        start_time = time.time()
        
        # Log request start
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown")
            }
        )
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log request completion
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": round(process_time, 4),
                "client_ip": request.client.host if request.client else "unknown"
            }
        )
        
        return response
