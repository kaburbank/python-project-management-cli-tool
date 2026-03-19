# Utility functions for validation and formatting
from dateutil.parser import parse as parse_date
import validators

def validate_email(email: str) -> bool:
    """
    Validate an email address using the validators library.
    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    return validators.email(email)

def parse_due_date(date_str: str):
    """
    Parse a due date string into a datetime object.
    Args:
        date_str (str): The date string to parse.
    Returns:
        datetime or None: Parsed datetime object if successful, None otherwise.
    """
    try:
        return parse_date(date_str)
    except Exception:
        return None
