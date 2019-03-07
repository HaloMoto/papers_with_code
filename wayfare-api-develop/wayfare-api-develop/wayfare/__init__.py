"""The main driver and entrypoint for the Wayfare API."""

import argparse
import flask_restful
import flask_sqlalchemy

from flask import Flask


DB_URI = 'sqlite:///./main.db'


app = Flask(__name__)  # pylint: disable=C0103
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = flask_sqlalchemy.SQLAlchemy(app)  # pylint: disable=C0103
# These imports are here to prevent errors from missing circular imports
from wayfare.models import Location  # pylint: disable=C0413
from wayfare.models import Status  # pylint: disable=C0413
from wayfare.models import TimeRange  # pylint: disable=C0413
from wayfare.models import User  # pylint: disable=C0413
from wayfare.models import Ride  # pylint: disable=C0413
from wayfare.models import Passenger  # pylint: disable=C0413
# Necessary for sqlite
db.drop_all()
db.create_all()

api = flask_restful.Api(app, catch_all_404s=True)  # pylint: disable=C0103
