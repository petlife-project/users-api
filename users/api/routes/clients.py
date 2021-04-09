from flask_restful import Resource
from flask_jwt_extended import jwt_required

from users.api.services.registration import RegistrationService
from users.api.services.update import UpdateService


class Clients(Resource):
    """ For registering and updating clients' data."""

    @staticmethod
    def post():
        service = RegistrationService()
        return service.register('client')

    @staticmethod
    @jwt_required
    def put():
        service = UpdateService()
        return service.update('client')
