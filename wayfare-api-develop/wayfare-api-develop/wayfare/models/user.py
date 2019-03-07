# pylint: disable=E1101
"""Class wrapping a user table."""
import re

from typing import TypeVar

from wayfare import db
from wayfare import models
from wayfare.exceptions import DuplicateEmailError
from wayfare.exceptions import InvalidEmailError
from wayfare.exceptions import InvalidFirstNameError
from wayfare.exceptions import InvalidLastNameError
from wayfare.models import AbstractModelBase


UserType = TypeVar('UserType', bound='User')
_MAX_LENGTH = 64
_INVALID_CHARS = r'[~!@#$%^&*()+=_`]'

class User(AbstractModelBase):
    """Data access object providing a static interface to a user table."""
    __tablename__ = models.tables.USER

    first_name = db.Column(db.String(_MAX_LENGTH))
    last_name = db.Column(db.String(_MAX_LENGTH))
    email = db.Column(db.String(_MAX_LENGTH))
    password = db.Column(db.String(_MAX_LENGTH))

    @db.validates('first_name')
    def validate_first_name(self, key: str, first_name: str):
        """Check that a first name is valid.

        Args:
            key (str): Dict key corresponding to the field being validated.
            first_name (str): Value provided to field.

        Raises:
            'InvalidFirstNameError': If the length of given first name is longer than 64
                                     or contains an invalid character.

        """
        if len(first_name) > _MAX_LENGTH:
            raise InvalidFirstNameError(first_name)

        if re.compile(_INVALID_CHARS).search(first_name):
            raise InvalidFirstNameError(first_name)

        return first_name

    @db.validates('last_name')
    def validate_last_name(self, key: str, last_name: str):
        """Check that a first name is valid.

        Args:
            key (str): Dict key corresponding to the field being validated.
            last_name (str): Value provided to field.

        Raises:
            'InvalidLastNameError': If the length of given first name is longer than 64
                                     or contains an invalid character.
        """
        if len(last_name) > _MAX_LENGTH:
            raise InvalidLastNameError(last_name)

        if re.compile(_INVALID_CHARS).search(last_name):
            raise InvalidLastNameError(last_name)

        return last_name

    @db.validates('email')
    def validate_email(self, key: str, email: str):
        """Check that an email is unique seems valid.

        Args:
            key (str): Dict key corresponding to the field being validated.
            email (str): Value provided to field.

        Return:
            str: Email if valid.

        Raises:
            `InvalidEmailError`: If the given email does not have exactly one '@' and a '.' after the '@'.
            `DuplicateEmailError`: If a user with the given email already exists.
        """
        # REGEX notes:
        #
        # ^@ = any char except @
        # \ = inhibit the specialness of character (aka escape character)
        # https://developers.google.com/edu/python/regular-expressions

        if not re.compile(r'[^@]+@[^@]+\.[^@]+').match(email):
            raise InvalidEmailError(email)

        if self.find_by_email(email):
            raise DuplicateEmailError(email)

        return email

    @staticmethod
    def find_by_id(user_id: int) -> UserType:
        """Look up a `User` by id.

        Args:
            id (int): id to match.

        Returns:
            User with the given id if found, None if not found.

        See:
        https://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get
        """
        return db.session.query(User).get(user_id)

    @staticmethod
    def find_by_email(email: str) -> UserType:
        """Look up a `User` by email.

        Args:
            email (str): email to match.

        Returns:
            `User` with the given email if found, None if not found.
        """
        return db.session.query(User).filter(User.email == email).first()

    def __repr__(self) -> str:
        """Return a string representation of this `User`."""
        return f'TODO'
