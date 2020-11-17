from flask_restful import abort
from flask.json import jsonify

from users.utils.db.adapter_factory import get_mongo_adapter
from users.api.body_parsers.factory import FACTORY
from users.utils.env_vars import SHOPS_COLLECTION


class RemovalService:
    """ Service for petshops to remove a service from their list of available ones
    """
    def __init__(self):
        self.parser = FACTORY.get_parser('service_removal')

    def remove(self):
        """ Gets the fields from the parser and calls the update method

            Args:
                The three field necessary for this operation are
                the username and password and the service_id to identify
                what is being removed from the list.

            Returns:
                The updated user object
        """
        doc = self.parser.fields
        updated_user = self._update_in_mongo(SHOPS_COLLECTION, doc)
        return jsonify(updated_user)

    @staticmethod
    def _update_in_mongo(collection, doc):
        mongo = get_mongo_adapter()
        try:
            return mongo.remove_service(collection, doc)

        except KeyError as error:
            abort(400, extra='Incorrect username or password.')

        except RuntimeError as error:
            abort(500, extra=f'Error when updating, {error}')
