# Utility functions for validation and formatting
from dateutil.parser import parse as parse_date
import validators

def validate_email(email: str) -> bool:
    return validators.email(email)

def parse_due_date(date_str: str):
    try:
        return parse_date(date_str)
    except Exception:
        return None
