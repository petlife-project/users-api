from flask_restful import abort

from users.api.body_parsers.factory import FACTORY
from users.utils.db.adapter_factory import get_mongo_adapter
from users.utils.env_vars import CLIENTS_COLLECTION, SHOPS_COLLECTION


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
                200 (status code): If no errors occur and user provided
                    the right credentials.
        """
        request_data = self.parser.fields
        collection = self.collections[request_data['type']]
        del request_data['type']
        db_data = self._get_from_mongo(collection, request_data['username'])
        self._validate_request_data(request_data, db_data)
        return 200

    @staticmethod
    def _get_from_mongo(collection, username):
        """ Gets the user object from MongoDB and removes all fields unnecessary
            for the authentication process

            Args:
                collection (str): Where to look, depends on the type of user
                username (str): The username to look for

            Returns:
                info_to_compare (dict): User object with only the fields
                    needed for authenticating, ie: username and password
        """
        mongo = get_mongo_adapter()
        db_data = mongo.get_user_information(collection, username)

        info_to_compare = {
            k : v for k,v in db_data.items() \
            if k in ('username', 'password')
        }
        return info_to_compare

    @staticmethod
    def _validate_request_data(request_data, db_data):
        """ Validates the user's request by comparing the data got from the DB
            with the one sent in the request. In practice, this only compares
            the password field, as getting here means the username at least is correct

            Args:
                request_data (dict): The data sent by the user in the request
                db_data (dict): The data gotten from the database

            Raises:
                HTTPException: Error code 401, Unauthorized, if the values don't match
        """
        for field in db_data.keys():
            if db_data[field] != request_data[field]:
                abort(401, extra='Invalid username or password')
