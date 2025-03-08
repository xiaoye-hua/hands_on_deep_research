# Logging System Documentation

This document explains how to use the logging system in the Hands-On Deep Research project.

## Overview

The project uses Python's built-in `logging` module with some custom utilities to provide a consistent logging experience across all components. The logging system is designed to be flexible and configurable, allowing you to control the verbosity of logs, where they are stored, and their format.

## Log Levels

The logging system uses the standard Python logging levels:

- **DEBUG (10)**: Detailed information, typically useful only for diagnosing problems.
- **INFO (20)**: Confirmation that things are working as expected.
- **WARNING (30)**: An indication that something unexpected happened, or may happen in the near future.
- **ERROR (40)**: Due to a more serious problem, the software has not been able to perform some function.
- **CRITICAL (50)**: A serious error, indicating that the program itself may be unable to continue running.

By default, the logging level is set to `INFO`, which means that all logs with level `INFO` and above will be captured.

## Log Output

By default, logs are output to:

1. **Console**: All logs are printed to the standard output.
2. **File**: All logs are also written to log files in the `logs` directory at the project root.

The log files use a rotating file handler, which means that when a log file reaches a certain size (default: 10 MB), it is rotated, and a new log file is created. The system keeps a certain number of backup log files (default: 5) before deleting the oldest ones.

## Using the Logging System

### Getting a Logger

To use the logging system in your code, you need to get a logger instance. The recommended way is to use the `get_logger` function from the `src.utils.logging_utils` module:

```python
from src.utils.logging_utils import get_logger

# Get a logger with a specific name (usually the module name)
logger = get_logger(__name__)

# Now you can use the logger
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

### Logging in Classes

For classes, it's recommended to create a logger instance in the `__init__` method:

```python
from src.utils.logging_utils import get_logger

class MyClass:
    def __init__(self):
        # Set up logger with the class's module and name
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    def my_method(self):
        self.logger.debug("Entering my_method")
        # Method implementation
        self.logger.debug("Exiting my_method")
```

### Logging Exceptions

When catching exceptions, it's good practice to log them with the `exc_info=True` parameter, which includes the stack trace in the log:

```python
try:
    # Some code that might raise an exception
    result = some_function()
except Exception as e:
    logger.error(f"Error in some_function: {str(e)}", exc_info=True)
    # Handle the exception
```

## Configuring the Logging System

### Changing Log Level

You can change the log level when setting up a logger:

```python
from src.utils.logging_utils import setup_logger
import logging

# Set up a logger with DEBUG level
logger = setup_logger("my_logger", log_level=logging.DEBUG)
```

Or you can change the log level of an existing logger:

```python
logger.setLevel(logging.DEBUG)
```

### Changing Log Format

You can customize the log format when setting up a logger:

```python
from src.utils.logging_utils import setup_logger

# Set up a logger with a custom format
logger = setup_logger(
    "my_logger",
    log_format="%(asctime)s - %(levelname)s - %(message)s",
    date_format="%Y-%m-%d %H:%M:%S"
)
```

### Changing Log File Location

You can specify a custom log directory and file name:

```python
from src.utils.logging_utils import setup_logger

# Set up a logger with a custom log file
logger = setup_logger(
    "my_logger",
    log_dir="/path/to/custom/logs",
    log_file="my_custom_log.log"
)
```

### Disabling File or Console Logging

You can disable file or console logging:

```python
from src.utils.logging_utils import setup_logger

# Disable file logging
logger = setup_logger("my_logger", log_to_file=False)

# Disable console logging
logger = setup_logger("my_logger", log_to_console=False)
```

## Advanced Configuration

For more advanced configuration, you can directly use the `setup_logger` function from the `src.utils.logging_utils` module:

```python
from src.utils.logging_utils import setup_logger
import logging

# Set up a logger with custom configuration
logger = setup_logger(
    name="my_logger",
    log_level=logging.DEBUG,
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    date_format="%Y-%m-%d %H:%M:%S",
    log_to_console=True,
    log_to_file=True,
    log_file="my_logger.log",
    log_dir="/path/to/custom/logs",
    max_bytes=10 * 1024 * 1024,  # 10 MB
    backup_count=5
)
```

## Default Configuration

The logging system uses the following default configuration:

- **Log Level**: INFO
- **Log Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Date Format**: `%Y-%m-%d %H:%M:%S`
- **Log Directory**: `<project_root>/logs`
- **Max Log File Size**: 10 MB
- **Backup Count**: 5

These defaults can be overridden when setting up a logger.

## Best Practices

1. **Use Appropriate Log Levels**: Use the appropriate log level for each message. For example, use `DEBUG` for detailed information, `INFO` for general information, `WARNING` for potential issues, `ERROR` for errors, and `CRITICAL` for critical errors.

2. **Include Contextual Information**: Include relevant contextual information in log messages to make them more useful for debugging.

3. **Log at Entry and Exit Points**: Log at the entry and exit points of important methods to help trace the flow of execution.

4. **Log Exceptions**: Always log exceptions with `exc_info=True` to include the stack trace.

5. **Use Structured Logging**: Consider using structured logging (e.g., including key-value pairs in log messages) to make logs more machine-readable and easier to analyze.

6. **Avoid Sensitive Information**: Be careful not to log sensitive information such as passwords, API keys, or personal data.

7. **Limit Log Size**: Be mindful of the size of log messages, especially when logging large objects or responses. Consider truncating long strings or using a summary instead.

## Example Usage

Here's a complete example of how to use the logging system:

```python
from src.utils.logging_utils import get_logger

# Get a logger
logger = get_logger(__name__)

def process_data(data):
    logger.info(f"Processing data with {len(data)} items")
    
    try:
        # Some processing logic
        result = [item * 2 for item in data]
        logger.debug(f"Processed data: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}", exc_info=True)
        raise

# Usage
try:
    data = [1, 2, 3, 4, 5]
    result = process_data(data)
    logger.info(f"Successfully processed data: {result}")
except Exception as e:
    logger.critical(f"Critical error in data processing: {str(e)}")
```

This example demonstrates how to get a logger, log at different levels, and handle exceptions with proper logging.

## Example Script

The project includes an example script at `examples/logging_example.py` that demonstrates the logging system in action. You can run this script to see how the logging system works:

```bash
cd examples
python logging_example.py
```

The script demonstrates:

1. Basic logging with different log levels
2. Logging in a class
3. Logging exceptions
4. Custom logger configuration

After running the script, you can check the `logs` directory to see the log files that were created. 