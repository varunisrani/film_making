"""
Logging utilities for tracking API calls and other operations.
"""
import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a logger
logger = logging.getLogger('film_making')

# Create a file handler
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
os.makedirs(logs_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(logs_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log"))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# In-memory storage for API call logs
api_logs = []

def log_api_call(
    provider: str,
    model: str,
    prompt_length: int,
    response_length: int,
    duration: float,
    status: str,
    error: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Log an API call to the in-memory storage and file.
    
    Args:
        provider: The API provider (e.g., 'openai', 'gemini')
        model: The model used
        prompt_length: The length of the prompt in characters
        response_length: The length of the response in characters
        duration: The duration of the API call in seconds
        status: The status of the API call ('success', 'error')
        error: The error message if status is 'error'
        metadata: Additional metadata about the API call
        
    Returns:
        The log entry that was created
    """
    timestamp = datetime.now().isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "provider": provider,
        "model": model,
        "prompt_length": prompt_length,
        "response_length": response_length,
        "duration": duration,
        "status": status,
    }
    
    if error:
        log_entry["error"] = error
    
    if metadata:
        log_entry["metadata"] = metadata
    
    # Add to in-memory storage
    api_logs.append(log_entry)
    
    # Log to file
    logger.info(f"API Call: {json.dumps(log_entry)}")
    
    return log_entry

def get_api_logs() -> List[Dict[str, Any]]:
    """Get all API call logs.
    
    Returns:
        A list of all API call logs
    """
    return api_logs

def clear_api_logs() -> None:
    """Clear all API call logs."""
    api_logs.clear()

def get_api_stats() -> Dict[str, Any]:
    """Get statistics about API calls.
    
    Returns:
        A dictionary containing statistics about API calls
    """
    if not api_logs:
        return {
            "total_calls": 0,
            "success_rate": 0,
            "avg_duration": 0,
            "providers": {},
            "models": {}
        }
    
    total_calls = len(api_logs)
    success_calls = sum(1 for log in api_logs if log["status"] == "success")
    success_rate = (success_calls / total_calls) * 100 if total_calls > 0 else 0
    
    # Calculate average duration for successful calls
    durations = [log["duration"] for log in api_logs if log["status"] == "success"]
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # Count by provider
    providers = {}
    for log in api_logs:
        provider = log["provider"]
        if provider not in providers:
            providers[provider] = 0
        providers[provider] += 1
    
    # Count by model
    models = {}
    for log in api_logs:
        model = log["model"]
        if model not in models:
            models[model] = 0
        models[model] += 1
    
    return {
        "total_calls": total_calls,
        "success_calls": success_calls,
        "success_rate": success_rate,
        "avg_duration": avg_duration,
        "providers": providers,
        "models": models
    }