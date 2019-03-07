# pylint: disable=E1101
"""Class wrapping a status table."""
from typing import TypeVar

from wayfare import db
from wayfare import models

from wayfare.models import AbstractModelBase


StatusType = TypeVar('StatusType', bound='Status')


class Status(AbstractModelBase):
    """Data access object providing a static interface to a status table."""
    __tablename__ = models.tables.STATUS

    description = db.Column(db.String(64))

    @staticmethod
    def find_by_id(status_id: int) -> StatusType:
        """Look up a `Status` by id.

        Args:
            status_id (int): id to match.

        Returns:
            `Status` with the given id if found, None if not found.
        """
        return db.session.query(Status).get(status_id)

    @staticmethod
    def find_by_description(description: str) -> StatusType:
        """Look up a `Status` by description.

        Args:
            description: (str): description to match.

        Returns:
            `Status` with the given description if found, None if not found.
        """
        return db.session.query(Status).filter(Status.description == description).first()

    def __repr__(self) -> str:
        """Return a string representation of this `Status`."""
        return f"Status({self.id}, '{self.description}')"

    def __str__(self) -> str:
        """Return this `Status` as a friendly string."""
        return f"{self.id}. {self.description}"
