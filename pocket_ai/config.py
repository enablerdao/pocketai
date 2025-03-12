"""
Configuration settings for ポケットAI (Pocket AI)
"""

import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    # LLM settings
    "llm": {
        "model": "claude-3-sonnet-20240229",
        "temperature": 0.7,
        "max_tokens": 2000,
        "api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    },
    
    # Browser settings
    "browser": {
        "type": "playwright",  # Options: "playwright", "selenium"
        "headless": True,
        "timeout": 30000,  # milliseconds
    },
    
    # Agent settings
    "agent": {
        "name": "ポケットAI",
        "description": "A Doraemon-inspired AI assistant that helps with programming tasks",
        "max_iterations": 10,
        "memory_size": 100,  # Number of messages to keep in memory
    },
    
    # Server settings
    "server": {
        "host": "0.0.0.0",
        "port": 54656,  # Use the provided port
    }
}

# User configuration (can be loaded from a file)
user_config: Dict[str, Any] = {}

# Merged configuration
config: Dict[str, Any] = {**DEFAULT_CONFIG, **user_config}

def get_config(key: str = None) -> Any:
    """Get configuration value by key or return the entire config if key is None"""
    if key is None:
        return config
    
    keys = key.split(".")
    value = config
    for k in keys:
        if k in value:
            value = value[k]
        else:
            return None
    
    return value

def update_config(key: str, value: Any) -> None:
    """Update configuration value by key"""
    keys = key.split(".")
    target = config
    
    # Navigate to the nested dictionary
    for k in keys[:-1]:
        if k not in target:
            target[k] = {}
        target = target[k]
    
    # Update the value
    target[keys[-1]] = value