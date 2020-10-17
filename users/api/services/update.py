import json

from flask_restful import abort
from flask.json import jsonify

from users.utils.db.adapter_factory import get_mongo_adapter, get_cos_adapter
from users.api.services.data_input import DataInputService


class UpdateService(DataInputService):
    """ Service for users to add and/or change their information
    """
    def __init__(self):
        self.validations = {
            'email': self._validate_email,
            'pets': self._validate_pets,
            'services': self._validate_services,
            'profile_pic': self._validate_pics,
            'banner_pic': self._validate_pics
        }

    def update(self, type_):
        """ Runs all necessary validations then updates the user object in MongoDB

            The validations occur based on whether
            the field has come in the request or not,
            that is, if the field was not sent, no validation
            is run for it.

            Args:
                type_ (str): Selects the type of user, meaning in which collection they're in
                Also, the fields allowed to be updated are in the parsers section

            Returns:
                doc (JSON): The updated user object
        """
        collection = self.types[type_]
        parser = self.parser_factory.get_parser(f'{type_}_update')
        doc = parser.fields
        self._validate_fields(doc)
        updated = self._update_in_mongo(collection, doc)
        return jsonify(updated)

    @staticmethod
    def _update_in_mongo(collection, doc):
        mongo = get_mongo_adapter()
        try:
            return mongo.update(collection, doc)

        except KeyError as error:
            abort(400, extra='Incorrect username or password.')

        except RuntimeError as error:
            abort(500, extra=f'Error when updating, {error}')

    @staticmethod
    def _validate_pets(doc):
        pets = json.loads(doc['pets'])
        # Future validations go here
        doc['pets'] = pets

    @staticmethod
    def _validate_services(doc):
        services = json.loads(doc['services'])
        # Future validations go here
        doc['services'] = services

    @staticmethod
    def _validate_pics(doc):
        doc['pics'] = {} if not doc.get('pics') else doc.get('pics')
        cos = get_cos_adapter()

        if doc.get('profile_pic'):
            doc['pics']['profile'] = cos.upload(doc['profile_pic'])
            del doc['profile_pic']

        if doc.get('banner_pic'):
            doc['pics']['banner'] = cos.upload(doc['banner_pic'])
            del doc['banner_pic']
