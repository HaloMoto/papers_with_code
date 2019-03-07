"""
This module contains utility functions used throughout the application.

If a function seems like it could be used in multiple places, put it here and import it by name in
all files using said function. That way if we need to update a function, we don't need to find all
definitions across the application.

Example:
    In this file:

        def cool_function(a: int) -> int:
            # Whatever

    At the top of the file using the function:

        from ..utils import cool_function

    (Depending on the location of the file, you may need more, less, or no dots.)
"""
import datetime
import json
import os

from typing import Any


_ROOT_DIR = 'wayfare'


def compare_datestrings(date_string_a: str, date_string_b: str) -> int:
    """Compares two date strings chronologically.

    Args:
        date_string_a (str): A date string.
        date_string_b (str): Another date string.

    Returns:
        int: a negative, zero or positive integer depending on whether the
        first date is before, the same as, or after the second date.
    """
    return compare_dates(datetime.datetime.strptime(date_string_a, '%Y-%m-%d'),
                         datetime.datetime.strptime(date_string_b, '%Y-%m-%d'))


def compare_dates(date_a: datetime.date, date_b: datetime.date) -> int:
    """Compares two dates chronologically.

    Args:
        date_a (date): A date.
        date_b (date): Another date.

    Returns:
        int: < 0 if the first date falls chronologically before the second date.
             > 0 if the first date falls chronologically after the second date.
             = 0 if the two dates are identical.
    """
    return date_b - date_a


def load_json(path: str) -> Any:
    """Loads JSON data from a filepath.

    Args:
        path (str): Path to Local JSON file.

    Returns:
        Contents of the JSON file.
    """
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def root_join(*path: str) -> str:
    """Constructs a filepath based on the application's root directory from variadic arguments.

    Args:
        path (str): Items (directories) in the path.

    Returns:
        String filepath.

    Example:
        On a Unix-based OS:
        root_join('test') -> '/path/to/wayfare-api/wayfare/test'

        On Windows: (-_-)
        root_join('data', 'test.json') -> '\\path\\to\\wayfare-api\\wayfare\\data\\test.json'
    """
    base = os.path.abspath(os.path.dirname(__name__))
    return os.path.join(base, _ROOT_DIR, *path)


def validate_iso_date(date_string: str) -> bool:
    """Validates that a date string is in ISO format.

    Args:
        date_string (str): A date string.

    Returns:
        bool: whether or not the date string can be interpreted as an ISO date.
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except TypeError:
        return False
    except ValueError:
        return False
