from flask_restful import abort
from flask.json import jsonify
from flask_jwt_extended import get_jwt_identity

from users.utils.db.adapter_factory import get_mongo_adapter
from users.api.body_parsers.factory import FACTORY
from users.utils.env_vars import SHOPS_COLLECTION


# pylint: disable=inconsistent-return-statements
class RemovalService:
    def __init__(self):
        self.parser = FACTORY.get_parser('service_removal')

    def remove(self):
        """ Gets the fields from the parser and calls the update method

            Args:
                The service_id to identify which one to remove from the list.

            Returns:
                The updated user object
        """
        doc = self.parser.fields
        updated_user = self._update_in_mongo(SHOPS_COLLECTION, doc)
        return jsonify(updated_user)

    @staticmethod
    def _update_in_mongo(collection, doc):
        mongo = get_mongo_adapter()
        user = get_jwt_identity()
        try:
            return mongo.remove_service(collection, doc, user['_id'])

        except KeyError as error:
            abort(404, extra=str(error))

        except RuntimeError as error:
            abort(500, extra=f'Error when updating, {error}')
