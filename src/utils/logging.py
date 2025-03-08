"""
Logging utility functions.

This module provides utility functions for setting up and configuring logging.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional, Union


def setup_logging(
    log_level: Union[str, int] = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Set up logging configuration.

    Args:
        log_level: The log level to use. Can be a string (e.g., 'INFO') or an int.
        log_file: Optional path to a log file. If not provided, logs will be output to stdout only.
        log_format: Optional custom log format. If not provided, a default format will be used.

    Returns:
        A configured logger instance.
    """
    # Convert string log level to numeric value if needed
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper())

    # Default log format
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Add file handler if log_file is provided
    if log_file:
        # Create log directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Use rotating file handler to prevent log files from growing too large
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Create and return main logger for the application
    logger = logging.getLogger("deep_research")
    logger.debug("Logging initialized.")
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name: The name for the logger.

    Returns:
        A logger instance.
    """
    return logging.getLogger(f"deep_research.{name}") 