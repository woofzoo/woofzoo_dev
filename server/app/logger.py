"""
Application-wide logging configuration using Loguru.

This module configures Loguru with sensible defaults for development and production.
"""

from __future__ import annotations

import sys
from typing import Any

from loguru import logger
from app.middleware.trace_id import get_trace_id


def _get_trace_id_for_logging() -> str:
    """Get trace ID for logging format string."""
    trace_id = get_trace_id().replace("-", "")
    return f"[{trace_id[:12]}]" if trace_id else "[no-trace]"


def _filter_traceback(record):
    """Filter traceback to show only application code."""
    if record.get("exception"):
        import traceback
        import sys
        
        # Get the exception info
        exc_type, exc_value, exc_traceback = record["exception"]
        
        # Create a filtered traceback that excludes framework code
        filtered_tb = []
        tb = exc_traceback
        
        while tb is not None:
            filename = tb.tb_frame.f_code.co_filename
            
            # Only include frames from our application code
            if any(path in filename for path in ["/app/", "\\app\\", "app/", "app\\"]):
                filtered_tb.append(tb)
            
            tb = tb.tb_next
        
        # If we have filtered frames, create a new traceback
        if filtered_tb:
            # Create a new traceback with only our application frames
            new_tb = filtered_tb[0]
            for tb in filtered_tb[1:]:
                new_tb.tb_next = tb
            
            # Update the record with the filtered traceback
            record["exception"] = (exc_type, exc_value, new_tb)
    
    return True


def configure_logging(debug: bool = False) -> None:
    """Configure Loguru sinks and formatting.

    Args:
        debug: Whether to enable debug/verbose logging.
    """
    # Remove default handlers to avoid duplicate logs when reloading
    logger.remove()

    # Console sink with loguru's native format string
    logger.add(
        sys.stderr,
        level="DEBUG" if debug else "INFO",
        enqueue=True,
        backtrace=True,  # Always show backtrace for exceptions
        diagnose=False,  # Disable verbose diagnosis
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {extra[trace_id]} | {name}:{function}:{line} - {message}",
        filter=lambda record: record.update(extra={"trace_id": _get_trace_id_for_logging()}) or True,
    )

    
    # Intercept standard library logging and redirect to loguru
    _intercept_standard_logging()


def _intercept_standard_logging():
    """Intercept standard library logging and redirect to loguru."""
    import logging
    
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where the logged message was emitted
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Replace handlers for all loggers
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False


