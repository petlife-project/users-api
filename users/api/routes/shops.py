from flask_restful import Resource

from users.api.services.registration import RegistrationService
from users.api.services.update import UpdateService


class Shops(Resource):
    """ For registering and updating shops' data."""

    @staticmethod
    def post():
        service = RegistrationService()
        return service.register('shop')

    @staticmethod
    def put():
        service = UpdateService()
        return service.update('shop')
