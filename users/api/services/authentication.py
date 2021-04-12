from flask_restful import abort
from flask.json import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity

from users.api.body_parsers.factory import FACTORY
from users.utils.db.adapter_factory import get_mongo_adapter
from users.utils.env_vars import CLIENTS_COLLECTION, SHOPS_COLLECTION


# pylint: disable=inconsistent-return-statements
class AuthenticationService:
    def __init__(self):
        self.collections = {
            'client': CLIENTS_COLLECTION,
            'shop': SHOPS_COLLECTION
        }
        self.parser_factory = FACTORY
        self.parser = self.parser_factory.get_parser('auth')

    def authenticate(self):
        """ Authenticates the user with the information they provided

            Args:
                The fields parsed can be found in the auth body parser,
                they include username, password and type, so the process
                knows where to look for that user

            Returns:
                db_data (json): The whole user object, except for the password
        """
        request_data = self.parser.fields
        collection = self.collections[request_data['type']]

        mongo = get_mongo_adapter()
        try:
            user = mongo.get_user_by_username(
                collection, request_data['username'], request_data['password']
            )
            return jsonify(create_access_token(user))
        except KeyError as error:
            abort(401, extra=str(error))

    def delete_user(self):
        user = get_jwt_identity()
        collection = self.collections[user['type']]

        mongo = get_mongo_adapter()
        mongo.delete(collection, user['_id'])
