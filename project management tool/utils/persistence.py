# JSON persistence for users, projects, and tasks
import json
import os
from typing import Any

def load_json(filename: str) -> Any:
    """Load JSON data from a file. Returns an empty dict if file is missing or malformed."""
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(filename: str, data: Any):
    """Save data as JSON to a file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
