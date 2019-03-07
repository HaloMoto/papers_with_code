"""Flask-RESTful resources for interacting with user data."""
import flask_restful
from flask_restful import abort
from flask_restful import fields as flask_fields
from flask_restful import marshal_with
from webargs import fields as webargs_fields
from webargs.flaskparser import parser
from webargs.flaskparser import use_args

from wayfare.exceptions import DuplicateEmailError
from wayfare.exceptions import InvalidEmailError
from wayfare.models.user import User

BASE_URL = '/users'

# Fields to include in a response body.
_response_schema = {  # pylint: disable=C0103
    'id': flask_fields.Integer,
    'first_name': flask_fields.String,
    'last_name': flask_fields.String,
    'email': flask_fields.String
}

def _make_request_schema(require_all: bool = False) -> dict:
    """Create an expected schema for a request body or query.

    Args:
        require_all (bool): True to require that all fields be present.
    """
    return {
        'first_name': webargs_fields.String(required=require_all),  # pylint: disable=E1101
        'last_name': webargs_fields.String(required=require_all),  # pylint: disable=E1101
        'email': webargs_fields.String(required=require_all),  # pylint: disable=E1101
        'password': webargs_fields.String(required=require_all)  # pylint: disable=E1101
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


class Users(flask_restful.Resource):
    """Resource for interacting with `User` data."""
    @marshal_with(_response_schema)
    def get(self):
        """Retrieve all users.

        NOTE: This method can be very memory-intensive and should not be used in production.
        """
        return list(User.get_all())

    @use_args(_make_request_schema(require_all=True))
    def post(self, request_body: dict):
        """Create a user.

        Args:
            request_body (dict): Data extracted from request body.
        """
        try:
            user = User(
                first_name=request_body['first_name'],
                last_name=request_body['last_name'],
                email=request_body['email'],
                password=request_body['password']
            )
            user.create()
            return '', 201, {'location': f'{BASE_URL}/{user.id}'}
        except DuplicateEmailError as ex:
            abort(400, message=ex.message)
        except InvalidEmailError as ex:
            abort(400, message=ex.message)

    def delete(self):
        """Delete all users.

        NOTE: This is (potentially) an incredibly destructive method. Be careful.
        """
        User.delete_all()
        return '', 200


class UserById(flask_restful.Resource):
    """Resource for interacting with user data based on a user id."""
    @marshal_with(_response_schema)
    def get(self, user_id: int):
        """Get a user resource by id.

        Args:
            user_id (int): id of the user to look up.

        Returns:
            User with the given id if found.
        """
        user = User.find_by_id(user_id)
        if not user:
            abort(404, message="User {} does not exist".format(user_id))
        return user

    # TODO: This method should not require all fields.
    @use_args(_make_request_schema(require_all=True))
    def put(self, request_body: dict, user_id: int):
        """Create or update a user resource by id.

        Args:
            request_body (dict): Data extracted from request body.
            user_id (int): user id provided in the uri path.
        """
        user = User.find_by_id(user_id)
        if user:
            user.update_instance(request_body)
            return '', 200
        user = User(**request_body)
        user.create()
        return '', 201

    def delete(self, user_id: int):
        """Delete user with the given id.

        Args:
            user_id (int): id of the user to delete
        """
        user = User.find_by_id(user_id)
        if user:
            user.delete_instance()
            return '', 200
        abort(404, message="User {} does not exist".format(user_id))
