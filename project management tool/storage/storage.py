# File IO and persistence logic
import json
from typing import Any

class Storage:
    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> Any:
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self, data: Any):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
