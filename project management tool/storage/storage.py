# File IO and persistence logic
import json
from typing import Any
import logging

class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.logger = logging.getLogger("storage")

    def load(self) -> Any:
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.logger.info(f"Loaded data from {self.filename}")
                return data
        except FileNotFoundError:
            self.logger.warning(f"File not found: {self.filename}, returning empty dict")
            return {}
        except json.JSONDecodeError:
            self.logger.error(f"Malformed JSON in {self.filename}, returning empty dict")
            return {}

    def save(self, data: Any):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Saved data to {self.filename}")
