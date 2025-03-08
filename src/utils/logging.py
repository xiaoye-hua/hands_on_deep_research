"""
Logging utilities.

This module provides functions for setting up logging in the project.
"""

import logging
import os
import sys
from typing import Optional, Union


def setup_logging(
    log_level: Union[str, int] = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Set up logging configuration.

    Args:
        log_level: The logging level. Can be a string (e.g., 'INFO') or an int (e.g., logging.INFO).
        log_file: Optional path to a log file. If not provided, logs will be output to console only.
        log_format: Optional custom log format. If not provided, a default format will be used.

    Returns:
        The configured logger.
    """
    # Convert string log level to numeric if necessary
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper())

    # Set up default log format if not provided
    if log_format is None:
        log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Set up file handler if log file is provided
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name: The name of the logger.

    Returns:
        The logger.
    """
    return logging.getLogger(name) 