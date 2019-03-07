# pylint: disable=E1101
"""Class wrapping a Passenger table."""
from typing import List, TypeVar

from wayfare import db
from wayfare import models
from wayfare.models import AbstractModelBase


PassengerType = TypeVar('PassengerType', bound='Location')

# TODO: Make this just a table, move functionality for passenger status into User and Ride models.


class Passenger(AbstractModelBase):
    """Data access object providing a static interface to a Passenger table."""
    __tablename__ = models.tables.PASSENGER

    # Column Attributes
    user_id = db.Column(db.Integer,
                        db.ForeignKey(models.tables.USER + '.id', ondelete='CASCADE'))
    ride_id = db.Column(db.Integer,
                        db.ForeignKey(models.tables.RIDE + '.id', ondelete='CASCADE'))
    status_id = db.Column(db.Integer,
                          db.ForeignKey(models.tables.STATUS + '.id'))


    # Relationship Attributes
    db.UniqueConstraint('user_id', 'ride_id', 'status_id')
    db.relationship('User',
                    uselist=False,
                    backref=db.backref('passenger', passive_deletes=True),
                    lazy='dynamic',
                    passive_deletes=True)
    db.relationship('Ride',
                    uselist=False,
                    backref=db.backref('passenger', passive_deletes=True),
                    lazy='dynamic',
                    passive_deletes=True)
    db.relationship('Status',
                    uselist=False,
                    lazy='dynamic')

    def update(self, new_status: int):
        """Update a passenger status by creating a new row.

        Args:
            new_status (int): id of new status.
        """
        # This should create a new row.
        pass

    @staticmethod
    def find_by_id(id: int) -> PassengerType:  # pylint: disable=C0103
        """Look up a `Passenger` by id.

        Args:
            id (int): id to match.

        Returns:
            `Passenger`s associated with the given id if found.
        """
        return db.session.query(Passenger).filter(Passenger.id == id).first()

    @staticmethod
    def find_by_ride_id(ride_id: int) -> List[PassengerType]:
        """Look up a `Passenger` by ride_id.

        Args:
            ride_id (int): id to match.

        Returns:
            `Passenger`s associated with the given ride_id if found.
        """
        return db.session.query(Passenger).filter(Passenger.ride_id == ride_id)

    @staticmethod
    def find_by_user_id(user_id: int) -> List[PassengerType]:
        """Look up a `Passenger` by user_id.

        Args:
            ride_id (int): id to match.

        Returns:
            `Passenger`s associated with the given user_id if found.
        """
        return db.session.query(Passenger).filter(Passenger.user_id == user_id)

    @staticmethod
    def find_by_status_id(status_id: int) -> List[PassengerType]:
        """Look up a `Passenger` by status_id.

        Args:
            status_id (int): id to match.

        Returns:
            `Passenger`s associated with the given status_id if found.
        """
        return db.session.query(Passenger).filter(Passenger.status_id == status_id)
