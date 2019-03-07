# pylint: disable=E1101
"""Class wrapping a time range table."""
from typing import TypeVar

from wayfare import db
from wayfare import models

from wayfare.models import AbstractModelBase


TimeRangeType = TypeVar('TimeRangeType', bound='TimeRange')


class TimeRange(AbstractModelBase):
    """Data access object providing a static interface to a time range table."""
    __tablename__ = models.tables.TIME_RANGE

    description = db.Column(db.String(255))
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)

    @staticmethod
    def find_by_id(time_range_id: int) -> TimeRangeType:
        """Look up a `TimeRange` by id.

        Args:
            time_range_id (int): id to match.

        Returns:
            TimeRange with the given id if found, None if not found.
        """
        return db.session.query(TimeRange).get(time_range_id)

    @staticmethod
    def find_by_start_time(start_time: int) -> TimeRangeType:
        """Look up a `TimeRange` by start time.

        Args:
            start_time (int): start time to match.

        Returns:
            TimeRange with the given start time if found, None if not found.
        """
        return db.session.query(TimeRange).filter(TimeRange.start_time == start_time).first()

    @staticmethod
    def find_by_end_time(end_time: int) -> TimeRangeType:
        """Look up a `Time Range` by end time.

        Args:
            end_time (int): end time to match.

        Returns:
            TimeRange with the given end time if found.
        """
        return db.session.query(TimeRange).filter(TimeRange.end_time == end_time).first()

    def __repr__(self) -> str:
        """Return a string representation of this `TimeRange`."""
        return f'TODO'
