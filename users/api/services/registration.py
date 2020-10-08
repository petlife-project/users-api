from flask_restful import abort
from flask.json import jsonify

from validate_docbr import CPF

from users.api.body_parsers.factory import FACTORY
from users.utils.db.adapter_factory import get_mongo_adapter
from users.utils.env_vars import CLIENTS_COLLECTION


class RegistrationService:
    """ Service responsible for registering new users, both clients and shops
    """
    def __init__(self):
        self.types = {
            'client': self._register_client
        }
        self.parser_factory = FACTORY

    def register(self, type_):
        """ Runs the proper method for the set type

            Args:
                type_ (str): Must be one of the available types in the types dict

            Returns:
                Method call
        """
        return self.types[type_]()

    def _register_client(self):
        """ Registers clients in their collection

            Args:
                The user object fields are parsed from
                the request's body, they can be found in
                the client model in this API's models directory

            Returns:
                New user document just inserted in the collection

            Raises:
                HttpException: 409 Conflict, if user already exists
        """
        collection = CLIENTS_COLLECTION
        parser = self.parser_factory.get_parser('client_registration')

        doc = parser.fields

        if doc['cpf']:
            self._validate_cpf(doc['cpf'])

        self._insert_in_mongo(collection, doc)
        return jsonify(doc)

    @staticmethod
    def _insert_in_mongo(collection, doc):
        mongo = get_mongo_adapter()
        try:
            mongo.create(collection, doc)
        except KeyError as error:
            abort(409, extra=f'{error}')

    @staticmethod
    def _validate_cpf(cpf):
        validator = CPF()
        valid = validator.validate(cpf)
        if valid:
            return
        abort(400, extra='Invalid CPF')
