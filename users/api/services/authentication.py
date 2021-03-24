from flask_restful import abort
from flask.json import jsonify

from users.api.body_parsers.factory import FACTORY
from users.utils.db.adapter_factory import get_mongo_adapter
from users.utils.env_vars import CLIENTS_COLLECTION, SHOPS_COLLECTION


# pylint: disable=inconsistent-return-statements
class AuthenticationService:
    """ Service for authentication, used in the login
    """
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
        del request_data['type']
        db_data = self._get_from_mongo(collection, request_data)
        return jsonify(db_data)

    @staticmethod
    def _get_from_mongo(collection, user):
        """ Gets the user object from MongoDB if username and password are correct
            and returns the whole object (except password field)
            for the creation of the user page. Or an error if the user is not found,
            meaning either the user or the password didn't match the information stored.

            Args:
                collection (str): Where to look, depends on the type of user
                user (dict): The user to look for

            Returns:
                user_object (dict): User object without password

            Raises:
                HTTPException: 401 Unauthorized if username or password don't match
        """
        mongo = get_mongo_adapter()
        username = user['username']
        password = user['password']

        try:
            return mongo.get_user_information(collection, username, password)

        except KeyError as error:
            abort(401, extra=f'{error}')
