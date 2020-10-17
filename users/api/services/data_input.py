import re

from flask_restful import abort

from users.api.body_parsers.factory import FACTORY
from users.utils.env_vars import CLIENTS_COLLECTION, SHOPS_COLLECTION


class DataInputService:
    """ Leveraging the concept of inheritance
        to group commom methods for the two data insertion services
    """
    parser_factory = FACTORY
    types = {
        'client': CLIENTS_COLLECTION,
        'shop': SHOPS_COLLECTION
    }
    validations = {}

    @staticmethod
    def _validate_email(doc):
        email = doc['email']

        if not re.match(r'\S+@\S+\.\S+', email):
            abort(400, extra='Invalid email address!')

    def _validate_fields(self, doc):
        for field in doc:
            if field in self.validations.keys():
                self.validations[field](doc)
