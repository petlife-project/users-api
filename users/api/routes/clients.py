from flask_restful import Resource
from flask_jwt_extended import jwt_required

from users.api.services.data_input import DataInputService


class Clients(Resource):
    """ For registering and updating clients' data."""

    @staticmethod
    def post():
        service = DataInputService()
        return service.register('client')

    @staticmethod
    @jwt_required
    def put():
        service = DataInputService()
        return service.update('client')
