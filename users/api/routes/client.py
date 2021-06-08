from flask_restful import Resource
from flask_jwt_extended import jwt_required

from users.api.services.data_input import DataInputService
from users.api.services.removal import RemovalService


class Client(Resource):
    """ For registering and updating client' data."""

    @staticmethod
    def post():
        service = DataInputService()
        return service.register('client')

    @staticmethod
    @jwt_required
    def put():
        service = DataInputService()
        return service.update('client')

    @staticmethod
    @jwt_required
    def delete():
        service = RemovalService()
        return service.remove('client')
