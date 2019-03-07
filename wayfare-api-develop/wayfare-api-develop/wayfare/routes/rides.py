"""Flask-RESTful resources for interacting with ride data."""
import flask_restful
from flask_restful import abort
from flask_restful import fields as flask_fields
from flask_restful import marshal_with
from webargs import fields as webargs_fields
from webargs.flaskparser import parser
from webargs.flaskparser import use_args

import dateutil.parser

from wayfare.exceptions import InvalidCapacityError
from wayfare.models import Ride

BASE_URL = '/rides'

# Fields to include in a response body.
_response_schema = {  # pylint: disable=C0103
    'id': flask_fields.Integer,
    'actual_departure_time': flask_fields.String,
    'departure_date': flask_fields.String,
    'capacity': flask_fields.Integer,
    'time_range_id': flask_fields.Integer,
    'driver_id': flask_fields.Integer,
    'start_location_id': flask_fields.Integer,
    'destination_id': flask_fields.Integer
}

_request_schema = {  # pylint: disable=C0103
    # Ride fields go here.
}

def _make_request_schema(require_all: bool = False) -> dict:
    """Create an expected schema for a request body or query.

    Args:
        require_all (bool): True to require that all fields be present.
    """
    return {
        'departure_date': webargs_fields.String(required=require_all),  # pylint: disable=E1101
        'capacity': webargs_fields.Integer(required=require_all),  # pylint: disable=E1101
        'time_range_id': webargs_fields.Integer(required=require_all),  # pylint: disable=E1101
        'driver_id': webargs_fields.Integer(required=require_all),  # pylint: disable=E1101
        'start_location_id': webargs_fields.Integer(required=require_all),  # pylint: disable=E1101
        'destination_id': webargs_fields.Integer(required=require_all)  # pylint: disable=E1101
    }

@parser.error_handler
def _handle_parse_error(err, req, schema):
    """Handler for request parse errors.

    This is called if a method decorated with `use_args` encounters a parse error.

    Args:
        err (webargs.core.ValidationError): Raised error.
        req (flask.Request): Flask request object.
        schema (marshmallow.Schema): Schema used to parse request.
    """
    abort(400, message=err.messages)


class Rides(flask_restful.Resource):
    """Resource for interacting with `Ride` data."""
    @marshal_with(_response_schema)
    def get(self):
        """Retrieve all rides.

        NOTE: This method can be very memory-intensive and should not be used in production.
        """
        return list(Ride.get_all())

    @use_args(_make_request_schema(require_all=True))
    def post(self, request_body: dict):
        """Create a ride.

        Args:
            request_body (dict): Data extracted from request body.
        """
        try:
            departure_date = dateutil.parser.parse(request_body['departure_date'])
            ride = Ride(
                departure_date=departure_date,
                capacity=request_body['capacity'],
                time_range_id=request_body['time_range_id'],
                driver_id=request_body['driver_id'],
                start_location_id=request_body['start_location_id'],
                destination_id=request_body['destination_id']
            )
            ride.create()
            return '', 201, {'location': f'{BASE_URL}/{ride.id}'}
        except InvalidCapacityError as ex:
            abort(400, message=ex.message)


    def delete(self):
        """Delete all rides.

        NOTE: This is (potentially) an incredibly destructive method. Be careful.
        """
        Ride.delete_all()
        return '', 200


class RidesById(flask_restful.Resource):
    """Resource for interacting with ride data based on a ride id."""
    @marshal_with(_response_schema)
    def get(self, ride_id: int):
        """Get a ride resource by id.

        Args:
            ride_id (int): id of the ride to look up.

        Returns:
            Ride with the given id if found.
        """
        ride = Ride.find_by_id(ride_id)
        if not ride:
            abort(404, message="Ride {} does not exist".format(ride_id))
        return ride

    # TODO: This method should not require all fields.
    @use_args(_make_request_schema(require_all=True))
    def put(self, request_body: dict, ride_id: int):
        """Create or update a ride resource by id.

        Args:
            request_body (dict): Data extracted from request body.
            ride_id (int): ride id provided in the uri path.
        """
        ride = Ride.find_by_id(ride_id)
        if ride:
            ride.update(request_body)
            return '', 200
        ride = Ride(**request_body)
        ride.create()
        return '', 201

    def delete(self, ride_id: int):
        """Delete ride with the given id.

        Args:
            ride_id (int): id of the ride to delete
        """
        ride = Ride.find_by_id(ride_id)
        if ride:
            ride.delete_instance()
            return '', 200
        abort(404, message="Ride {} does not exist".format(ride_id))
