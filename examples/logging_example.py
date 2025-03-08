"""
Example script demonstrating the logging system in the Hands-On Deep Research project.

This script shows how to use the logging system in different scenarios.
"""

import logging
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.logging_utils import get_logger, setup_logger, DEFAULT_LOG_DIR

# Example 1: Basic logging
def basic_logging_example():
    print("\n=== Example 1: Basic Logging ===")
    
    # Get a logger with the default configuration
    logger = get_logger("examples.basic")
    
    # Log messages at different levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

# Example 2: Logging in a class
class LoggingExample:
    def __init__(self):
        # Set up logger with the class's module and name
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    def do_something(self, value):
        self.logger.debug(f"Entering do_something with value: {value}")
        
        try:
            # Some processing logic
            result = value * 2
            self.logger.info(f"Processed value: {value} -> {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error in do_something: {str(e)}", exc_info=True)
            raise
        finally:
            self.logger.debug("Exiting do_something")

def class_logging_example():
    print("\n=== Example 2: Class Logging ===")
    
    example = LoggingExample()
    result = example.do_something(42)
    print(f"Result: {result}")

# Example 3: Logging exceptions
def exception_logging_example():
    print("\n=== Example 3: Exception Logging ===")
    
    logger = get_logger("examples.exceptions")
    
    try:
        # Some code that will raise an exception
        logger.info("Attempting to divide by zero")
        result = 1 / 0
    except Exception as e:
        logger.error(f"Error dividing by zero: {str(e)}", exc_info=True)
        print("Exception caught and logged")

# Example 4: Custom logger configuration
def custom_logger_example():
    print("\n=== Example 4: Custom Logger Configuration ===")
    
    # Set up a logger with custom configuration
    custom_log_file = os.path.join(DEFAULT_LOG_DIR, "custom_example.log")
    logger = setup_logger(
        name="examples.custom",
        log_level=logging.DEBUG,
        log_format="%(asctime)s - %(levelname)s - %(message)s",
        date_format="%Y-%m-%d %H:%M:%S",
        log_to_console=True,
        log_to_file=True,
        log_file="custom_example.log",
        max_bytes=1024 * 1024,  # 1 MB
        backup_count=3
    )
    
    logger.debug("This is a debug message with custom format")
    logger.info("This is an info message with custom format")
    logger.warning("This is a warning message with custom format")
    
    print(f"Custom logs are saved to {custom_log_file}")

# Run all examples
if __name__ == "__main__":
    print("Running logging examples...")
    print(f"Logs will be saved to: {DEFAULT_LOG_DIR}")
    
    basic_logging_example()
    class_logging_example()
    exception_logging_example()
    custom_logger_example()
    
    print("\nAll examples completed. Check the logs directory for log files.") 