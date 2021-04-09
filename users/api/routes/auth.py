from flask_restful import Resource
from flask_jwt_extended import jwt_required

from users.api.services.authentication import AuthenticationService


class Auth(Resource):
    """ Route for authenticating the user into the front end apps
    """

    @staticmethod
    def post():
        service = AuthenticationService()
        return service.authenticate()

    @staticmethod
    @jwt_required
    def delete():
        service = AuthenticationService()
        return service.delete_user()
