from flask_restful import abort
from flask.json import jsonify
from flask_jwt_extended import get_jwt_identity

from users.utils.db.adapter_factory import get_mongo_adapter
from users.api.body_parsers.factory import FACTORY
from users.utils.env_vars import CLIENTS_COLLECTION, SHOPS_COLLECTION


# pylint: disable=inconsistent-return-statements
class RemovalService:
    def __init__(self):
        self.parser_factory = FACTORY
        self.collections = {
            'client': CLIENTS_COLLECTION,
            'shop': SHOPS_COLLECTION
        }
        self.parser_type = {
            'client': 'pet_removal',
            'shop': 'service_removal'
        }

    def remove(self, type_):
        """ Removes one item from the array fields (pets and services)
            according to the user type

            Args:
                type_ (str): The user type

            Returns:
                The updated user object
        """
        collection = self.collections[type_]
        parser = self.parser_factory.get_parser(self.parser_type[type_])
        doc = parser.fields

        mongo = get_mongo_adapter()
        user = get_jwt_identity()
        try:
            updated_user = mongo.remove(collection, doc, user['_id'])
            return jsonify(updated_user)

        except KeyError as error:
            abort(404)

        except RuntimeError as error:
            abort(500, extra=f'Error when updating, {error}')
