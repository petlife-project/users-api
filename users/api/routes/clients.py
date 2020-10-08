from flask_restful import Resource

from users.api.services.registration import RegistrationService


class Clients(Resource):
    """ For registering and updating clients' data."""

    @staticmethod
    def post():
        service = RegistrationService()
        return service.register('client')

    @staticmethod
    def put():
        pass
