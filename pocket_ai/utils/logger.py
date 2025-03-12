"""
Logger utility for ポケットAI (Pocket AI)
"""

import logging
import sys
from typing import Optional

# Configure logging format
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure logging level
DEFAULT_LEVEL = logging.INFO

# Create a dictionary to store loggers
loggers = {}

def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a logger with the given name
    
    Args:
        name: The name of the logger
        level: Optional logging level
        
    Returns:
        A configured logger
    """
    global loggers
    
    if name in loggers:
        return loggers[name]
    
    # Create a new logger
    logger = logging.getLogger(name)
    logger.setLevel(level or DEFAULT_LEVEL)
    
    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level or DEFAULT_LEVEL)
    
    # Create a formatter
    formatter = logging.Formatter(LOGGING_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(console_handler)
    
    # Store the logger
    loggers[name] = logger
    
    return logger