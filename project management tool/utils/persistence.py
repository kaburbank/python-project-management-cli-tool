# JSON persistence for users, projects, and tasks
import json
import os
import logging
from typing import Any

def load_json(filename: str) -> Any:
    """Load JSON data from a file. Returns an empty dict if file is missing or malformed."""
    logger = logging.getLogger("persistence")
    if not os.path.exists(filename):
        logger.warning(f"File not found: {filename}, returning empty dict")
        return {}
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
            logger.info(f"Loaded data from {filename}")
            return data
        except json.JSONDecodeError:
            logger.error(f"Malformed JSON in {filename}, returning empty dict")
            return {}

def save_json(filename: str, data: Any):
    """Save data as JSON to a file."""
    logger = logging.getLogger("persistence")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved data to {filename}")
