# pylint: disable=E1101
"""Class wrapping a location table."""
from typing import TypeVar

from wayfare import db
from wayfare import models

from wayfare.models import AbstractModelBase


LocationType = TypeVar('LocationType', bound='Location')


class Location(AbstractModelBase):
    """Data access object providing a static interface to a location table."""
    __tablename__ = models.tables.LOCATION

    name = db.Column(db.String(128))
    db.UniqueConstraint('name')

    @staticmethod
    def find_by_id(location_id: int) -> LocationType:
        """Look up a `Location` by id.

        Args:
            location_id (int): id to match.

        Returns:
            `Location` with the given id if found, None if not found.
        """
        return db.session.query(Location).get(location_id)

    @staticmethod
    def find_by_name(name: str) -> LocationType:
        """Look up a `Location` by name.

        Args:
            name (str): name to match.

        Returns:
            `Location` with the given name if found, None if not found.
        """
        return db.session.query(Location).filter(Location.name == name).first()

    def __repr__(self) -> str:
        """Return a string representation of this `Location`."""
        return f"Location({self.id}, '{self.name}')"

    def __str__(self) -> str:
        """Return this `Location` as a friendly string."""
        return f"{self.id}. {self.name}"
