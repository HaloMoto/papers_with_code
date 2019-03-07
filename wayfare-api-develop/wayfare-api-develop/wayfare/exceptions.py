"""Exceptions raised by Wayfare API routes and models."""

class WayfareError(Exception):
    """Base Exception class for all user-defined errors."""
    pass

class DuplicateEmailError(WayfareError):
    """Exception indicating that a `User` email already exists.

    Attributes:
        email (str): Duplicate email that raised this exception.
    """
    def __init__(self, email: str):
        """Init `DuplicateEmailError` with the given email."""
        self.email = email
        self.message = "Duplicate email: '{}'".format(email)
        super().__init__(self.message)

class InvalidEmailError(WayfareError):
    """Exception raised when a provided email value is invalid.

    Attributes:
        email (str): Invalid email that raised this exception.
    """
    def __init__(self, email: str):
        """Init `DuplicateEmailError` with the given email."""
        self.email = email
        self.message = "Invalid email: '{}'".format(email)
        super().__init__(self.message)

class InvalidFirstNameError(WayfareError):
    """Exception raised when length of provided first name is invalid."""

    def __init__(self, first_name: str):
        self.first_name = first_name
        self.message = "Invalid first name: '{}'".format(first_name)
        super().__init__(self.message)

class InvalidLastNameError(WayfareError):
    """Exception raised when length of provided last name is invalid."""

    def __init__(self, last_name: str):
        self.last_name = last_name
        self.message = "Invalid last name: '{}'".format(last_name)
        super().__init__(self.message)

# for ride.py
class InvalidCapacityError(WayfareError):
    """Exception raised capacity is larger than 8."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.message = "Invalid capacity: '{}'".format(capacity)
        super().__init__(self.message)
