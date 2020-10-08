from flask_restful import Resource

from users.api.services.registration import RegistrationService


class Shops(Resource):
    """ For registering and updating shops' data."""

    @staticmethod
    def post():
        service = RegistrationService()
        return service.register('shop')

    @staticmethod
    def put():
        pass
