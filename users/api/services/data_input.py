import re

from flask_restful import abort
from flask.json import jsonify
from flask_jwt_extended import get_jwt_identity
from validate_docbr import CNPJ, CPF

from users.api.body_parsers.factory import FACTORY
from users.utils.db.adapter_factory import get_mongo_adapter, get_cos_adapter
from users.utils.env_vars import CLIENTS_COLLECTION, SHOPS_COLLECTION


class DataInputService:
    """ Service for inputing user data into the system,
        by registering a new user or updating an existing one
    """
    def __init__(self):
        self.parser_factory = FACTORY
        self.types = {
            'client': CLIENTS_COLLECTION,
            'shop': SHOPS_COLLECTION
        }
        self.validations = {
            'email': self._validate_email,
            'cpf': self._validate_cpf,
            'cnpj': self._validate_cnpj,
            'profile_pic': self._validate_pics,
            'banner_pic': self._validate_pics
        }

    def register(self, type_):
        """ Registers a new user on the app

            It validates the fields that require validation and
            creates the array fields for each type of user, saving it
            on the database and returning the new user afterwards

            Args:
                type_ (str): The type of user, hardcoded for each route

            Returns:
                (dict/JSON): The newly created user
        """
        collection = self.types[type_]
        parser = self.parser_factory.get_parser(f'{type_}_registration')
        doc = parser.fields
        self._validate_fields(doc)
        self._create_array_fields(doc, type_)
        doc['type'] = type_

        mongo = get_mongo_adapter()
        try:
            mongo.create(collection, doc)
        except KeyError as error:
            abort(409, extra=f'{error}')

        return jsonify(doc)

    def update(self, type_):
        """ Updates a user with the sent properties

            Validates any fields if required and saves it
            on the database, returning the updated user object
            to the requester

            Args:
                type_ (str): The type of user, hardcoded for each route

            Returns:
                (dict/JSON): The updated user
        """
        collection = self.types[type_]
        parser = self.parser_factory.get_parser(f'{type_}_update')
        doc = parser.fields
        self._validate_fields(doc)

        mongo = get_mongo_adapter()
        user = get_jwt_identity()
        try:
            updated = mongo.update(collection, doc, user['_id'])
            return jsonify(updated)

        except KeyError as error:
            abort(404, extra=str(error))

        except RuntimeError as error:
            abort(500, extra=f'Error when updating, {error}')

    @staticmethod
    def _create_array_fields(doc, type_):
        if type_ == 'client':
            doc['pets'] = []
        if type_ == 'shop':
            doc['services'] = []

    def _validate_fields(self, doc):
        for field in doc:
            if field in self.validations.keys():
                self.validations[field](doc)

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

    @staticmethod
    def _validate_email(doc):
        email = doc['email']

        if not re.match(r'\S+@\S+\.\S+', email):
            abort(400, extra='Invalid email address!')

    @staticmethod
    def _validate_cpf(doc):
        validator = CPF()
        valid = validator.validate(doc['cpf'])
        if valid:
            return
        abort(400, extra='Invalid CPF')

    @staticmethod
    def _validate_cnpj(doc):
        validator = CNPJ()
        valid = validator.validate(doc['cnpj'])
        if valid:
            return
        abort(400, extra='Invalid CNPJ')
