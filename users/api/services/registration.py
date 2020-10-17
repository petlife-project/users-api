from flask_restful import abort
from flask.json import jsonify

from validate_docbr import CNPJ, CPF

from users.utils.db.adapter_factory import get_mongo_adapter
from users.api.services.data_input import DataInputService


class RegistrationService(DataInputService):
    """ Service responsible for registering new users, both clients and shops
    """
    def __init__(self):
        self.validations = {
            'email': self._validate_email,
            'cpf': self._validate_cpf,
            'cnpj': self._validate_cnpj
        }

    def register(self, type_):
        """ Runs the proper method for the set type

            Args:
                type_ (str): Must be one of the available types in the types dict

            Returns:
                Method call
        """
        collection = self.types[type_]
        parser = self.parser_factory.get_parser(f'{type_}_registration')
        doc = parser.fields
        self._validate_fields(doc)
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
