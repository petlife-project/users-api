from flask_restful import Resource
from flask_jwt_extended import jwt_required

from users.api.services.data_input import DataInputService
from users.api.services.removal import RemovalService
from users.api.services.get_all import GetAllService


class Shops(Resource):
    """ For registering and updating shops' data."""

    @staticmethod
    @jwt_required
    def get():
        service = GetAllService()
        return service.get()

    @staticmethod
    def post():
        service = DataInputService()
        return service.register('shop')

    @staticmethod
    @jwt_required
    def put():
        service = DataInputService()
        return service.update('shop')

    @staticmethod
    @jwt_required
    def delete():
        service = RemovalService()
        return service.remove()
