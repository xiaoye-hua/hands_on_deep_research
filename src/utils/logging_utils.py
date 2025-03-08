"""
Logging utilities for the project.

This module provides functions to set up and configure logging for the project.
It includes functions to create loggers, set log levels, and configure log handlers.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional, Union

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Default log format
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# Default date format
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# Default log level
DEFAULT_LOG_LEVEL = logging.INFO
# Default log directory (absolute path)
DEFAULT_LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
# Default log file
DEFAULT_LOG_FILE = "hands_on_deep_research.log"
# Default max log file size (10 MB)
DEFAULT_MAX_BYTES = 10 * 1024 * 1024
# Default number of backup log files
DEFAULT_BACKUP_COUNT = 5

# Create logs directory if it doesn't exist
if not os.path.exists(DEFAULT_LOG_DIR):
    os.makedirs(DEFAULT_LOG_DIR)
    print(f"Created logs directory at: {DEFAULT_LOG_DIR}")


def setup_logger(
    name: str,
    log_level: Union[int, str] = DEFAULT_LOG_LEVEL,
    log_format: str = DEFAULT_LOG_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
    log_to_console: bool = True,
    log_to_file: bool = True,
    log_file: Optional[str] = None,
    log_dir: str = DEFAULT_LOG_DIR,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
) -> logging.Logger:
    """
    Set up a logger with the specified configuration.

    Args:
        name: The name of the logger.
        log_level: The log level (default: INFO).
        log_format: The log format (default: "%(asctime)s - %(name)s - %(levelname)s - %(message)s").
        date_format: The date format (default: "%Y-%m-%d %H:%M:%S").
        log_to_console: Whether to log to console (default: True).
        log_to_file: Whether to log to file (default: True).
        log_file: The log file name (default: None, which uses the logger name).
        log_dir: The log directory (default: "logs").
        max_bytes: The maximum log file size in bytes (default: 10 MB).
        backup_count: The number of backup log files (default: 5).

    Returns:
        The configured logger.
    """
    # Convert string log level to int if necessary
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper(), DEFAULT_LOG_LEVEL)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(log_format, date_format)

    # Add console handler if requested
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler if requested
    if log_to_file:
        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Created log directory: {log_dir}")

        # Use logger name as log file if not specified
        if log_file is None:
            log_file = f"{name.replace('.', '_')}.log"

        # Create log file path
        log_file_path = os.path.join(log_dir, log_file)

        # Create file handler
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    If the logger doesn't exist, it will be created with default settings.
    
    Args:
        name: The name of the logger.
        
    Returns:
        The logger.
    """
    logger = logging.getLogger(name)
    
    # If the logger doesn't have any handlers, set it up with default settings
    if not logger.handlers:
        logger = setup_logger(name)
        
    return logger


# Set up the root logger
root_logger = setup_logger("hands_on_deep_research") 