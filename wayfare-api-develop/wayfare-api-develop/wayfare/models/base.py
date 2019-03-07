# pylint: disable=E1101
"""Base model providing data access methods."""
from typing import List
from typing import TypeVar

from wayfare import db


T = TypeVar('T', bound='AbstractModelBase')


class AbstractModelBase(db.Model):
    """Abstract base class for SQLAlchemy models.

    Defines basic fields and generic create, update, delete, and aggregate table operations for application models.

    Defines the following fields:
        id (int): Auto-incrementing primary key id.
        date_created (datetime.datetime): Timestamp of model creation.
        date_modified (datetime.datetime): Timestamp of last model update.
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def create(self):
        """Add this model instance to the database."""
        db.session.add(self)
        db.session.commit()

    def update_instance(self, new_fields: dict):
        """Update this model instance in the database.

        Args:
            new_fields (dict): Dict containing new values for this `User`.
        """
        db.session.query(self.__class__).filter_by(id=self.id).update(new_fields)
        db.session.commit()

    def delete_instance(self):
        """Delete this model instance from the database."""
        db.session.query(self.__class__).filter_by(id=self.id).delete()
        db.session.commit()

    @classmethod
    def get_all(cls) -> List[T]:
        """Iterate through all model instances in the database.

        NOTE: This method can be very memory-intensive and should not be used in production.

        Yields:
            Next instance of this model in the database.
        """
        for model in db.session.query(cls):
            yield model

    @classmethod
    def delete_all(cls):
        """Delete all instances of this model in the database.

        NOTE: This method is incredibly desctructive and should not be used in production.
        """
        db.session.query(cls).delete()
        db.session.commit()
