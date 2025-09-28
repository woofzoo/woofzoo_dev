"""
Application-wide logging configuration using Loguru.

This module configures Loguru with sensible defaults for development and production.
"""

from __future__ import annotations

import sys
from typing import Any

from loguru import logger


def configure_logging(debug: bool = False) -> None:
    """Configure Loguru sinks and formatting.

    Args:
        debug: Whether to enable debug/verbose logging.
    """
    # Remove default handlers to avoid duplicate logs when reloading
    logger.remove()

    # Console sink
    logger.add(
        sys.stderr,
        level="DEBUG" if debug else "INFO",
        enqueue=True,
        backtrace=debug,
        diagnose=debug,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | "
            "{name}:{function}:{line} - {message}"
        ),
    )

    # Optionally, add a rotating file sink in production or when needed
    # Example (disabled by default):
    # logger.add(
    #     "logs/app.log",
    #     rotation="10 MB",
    #     retention="14 days",
    #     compression="zip",
    #     level="INFO",
    #     enqueue=True,
    # )


