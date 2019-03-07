# pylint: disable=E1101
"""Class wrapping a Ride table."""
from typing import List, TypeVar

from datetime import datetime

from wayfare import db
from wayfare import models

from wayfare.exceptions import InvalidCapacityError
from wayfare.models import AbstractModelBase
from wayfare.models import Location
from wayfare.models import TimeRange
from wayfare.models import User
from wayfare.models import Passenger


RideType = TypeVar('RideType', bound='Ride')
_MAX_CAPACITY = 8  # assuming 8 seats are reasonable number excluding driver


class Ride(AbstractModelBase):
    """Data access object providing a static interface to a Ride table."""
    __tablename__ = models.tables.RIDE

    # Column Attributes
    #actual_departure_time and departure_date were originally db.DateTime
    #but changed to db.String for the purpose of just getting this fucking thing to work
    #
    actual_departure_time = db.Column(db.DateTime)
    departure_date = db.Column(db.DateTime)
    capacity = db.Column(db.Integer)
    time_range_id = db.Column(db.Integer,
                              db.ForeignKey(models.tables.TIME_RANGE + '.id'),
                              nullable=False)
    driver_id = db.Column(db.Integer,
                          db.ForeignKey(models.tables.USER + '.id'),
                          nullable=False)
    start_location_id = db.Column(db.Integer,
                                  db.ForeignKey(models.tables.LOCATION + '.id'),
                                  nullable=False)
    destination_id = db.Column(db.Integer,
                               db.ForeignKey(models.tables.LOCATION + '.id'),
                               nullable=False)

    # Relationship Attributes
    time_range = db.relationship(TimeRange)
    driver = db.relationship(User, backref='drives', lazy=True)
    passengers = db.relationship(Passenger, cascade="all, delete-orphan")
    start_location = db.relationship(Location, foreign_keys=[start_location_id])
    destination = db.relationship(Location, foreign_keys=[destination_id])

    @db.validates('capacity')
    def validate_capacity(self, key: str, capacity: str):
        """Check that capacity is valid.

        Args:
            capacity (str): Value provided to field.

        Return:
            int: capacity if valid.

        Raises:
            `InvalidCapacityError`: If the given capacity is not an int or greater than max.
        """
        if int(capacity) > _MAX_CAPACITY:
            raise InvalidCapacityError(capacity)

        if not str(capacity).isdigit():
            raise InvalidCapacityError(capacity)

        return int(capacity)

    # @db.validates('time_range')
    # TODO

    # @db.validates('driver')
    # TODO

    # I actually don't know if this is supposed to be validating 'start_location' or 'start_location_id'.
    @db.validates('start_location')
    def validate_start_location(self, key: str, start_location: str):
        """Check that a start location is valid.

        Args:
            start_location (str): Value provided to field.

        Return:
            int: start location id if valid.
        """
        # TODO
        return start_location

    # See start_location
    # @db.validates('destination')
    # TODO


    @staticmethod
    def find_by_id(ride_id: int) -> RideType:
        """Look up a `Ride` by id.

        Args:
            id (int): id to match.

        Returns:
            Ride with the given id if found.
        """
        return db.session.query(Ride).filter(Ride.id == ride_id).first()

    @staticmethod
    def find_by_departure_date(departure_date: datetime) -> List[RideType]:
        """Look up a `Ride` by departure date.

        Args:
            departure_date (datetime): id to match.

        Returns:
            `Ride`s associated with the given departure date if found.
        """
        return db.session.query(Ride).filter(Ride.departure_date == departure_date)

    @staticmethod
    def find_by_actual_departure_time(actual_departure_time: datetime) -> List[RideType]:
        """Look up a `Ride` by actual departure time.

        Args:
            actual_departure_time (datetime): id to match.

        Returns:
            `Ride`s associated with the given actual departure time if found.
        """
        return db.session.query(Ride).filter(Ride.actual_departure_time == actual_departure_time)

    @staticmethod
    def find_by_time_range_id(time_range_id: int) -> List['Ride']:
        """Look up a `Ride` by time_range_id.

        Args:
            time_range_id (int): id to match.

        Returns:
            `Ride`s associated with the given time_range_id if found.
        """
        return db.session.query(Ride).filter(Ride.time_range_id == time_range_id)

    @staticmethod
    def find_by_driver_id(driver_id: int) -> List['Ride']:
        """Look up a `Ride` by driver_id.

        Args:
            driver_id (int): id to match.

        Returns:
            `Ride`s associated with the given driver_id if found.
        """
        return db.session.query(Ride).filter(Ride.driver_id == driver_id)

    @staticmethod
    def find_by_start_location_id(start_location_id: int) -> List[RideType]:
        """Look up a `Ride` by start_location_id.

        Args:
            start_location_id (int): id to match.

        Returns:
            `Ride`s associated with the given start_location_ idif found.
        """
        return db.session.query(Ride).filter(Ride.start_location_id == start_location_id)

    @staticmethod
    def find_by_destination_id(destination_id: int) -> List[RideType]:
        """Look up a `Ride` by destination_id.

        Args:
            destination (int): id to match.

        Returns:
            `Ride`s associated with the given destination_id if found.
        """
        return db.session.query(Ride).filter(Ride.destination_id == destination_id)

    def __repr__(self) -> str:
        """Return a string representation of this `Ride`."""
        return f'TODO'
