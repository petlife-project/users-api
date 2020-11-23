from flask_restful import Resource

from users.api.services.authentication import AuthenticationService


class Auth(Resource):
    """ Route for authenticating the user into the front end apps
    """

    @staticmethod
    def post():
        service = AuthenticationService()
        return service.authenticate()
