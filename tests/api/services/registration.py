import unittest
from unittest.mock import MagicMock, patch

from werkzeug.exceptions import HTTPException

from users.api.services.registration import RegistrationService


# pylint: disable=protected-access
class RegistrationServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.registration.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('users.api.services.registration.jsonify')
        self.mocks['jsonify_mock'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        cpf_patch = patch('users.api.services.registration.CPF')
        self.mocks['cpf_mock'] = cpf_patch.start()
        self.patches.append(cpf_patch)

        cnpj_patch = patch('users.api.services.registration.CNPJ')
        self.mocks['cnpj_mock'] = cnpj_patch.start()
        self.patches.append(cnpj_patch)

        mongo_patch = patch('users.api.services.registration.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        data_input_patch = patch('users.api.services.registration.DataInputService')
        self.mocks['data_input_mock'] = data_input_patch.start()
        self.patches.append(data_input_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_sets_validations(self):
        # Setup
        mock_self = MagicMock(
            _validate_email='method1',
            _validate_cpf='method2',
            _validate_cnpj='method3'
        )

        # Act
        RegistrationService.__init__(mock_self)

        # Assert
        self.assertDictEqual(
            mock_self.validations,
            {
                'email': 'method1',
                'cpf': 'method2',
                'cnpj': 'method3'
            }
        )

    @staticmethod
    def test_register_returns_new_user():
        # Setup
        new_user = {
            'new': 'user',
            'right': 'here'
        }
        mock_self = MagicMock(types={'test_type': 'test_col'})
        mock_self.parser_factory.get_parser.return_value = \
            MagicMock(fields=new_user)
        type_ = 'test_type'

        # Act
        RegistrationService.register(mock_self, type_)

        # Assert
        mock_self._validate_fields.assert_called_with(new_user)
        mock_self._create_array_fields.assert_called_with(
            new_user, 'test_type'
        )
        mock_self._insert_in_mongo.assert_called_with(
            'test_col', new_user
        )

    def test_insert_in_mongo_user_is_created(self):
        # Setup
        collection = 'test_col'
        doc = {'some': 'user'}

        # Act
        RegistrationService._insert_in_mongo(collection, doc)

        # Assert
        self.mocks['mongo_mock'].return_value.\
            create.assert_called_with(
                'test_col', {'some': 'user'}
            )

    def test_insert_in_mongo_duplicated_user_abort(self):
        # Setup
        collection = 'test_col'
        doc = {'some': 'user'}
        self.mocks['mongo_mock'].return_value.\
            create.side_effect = KeyError('error_message')
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            RegistrationService._insert_in_mongo(collection, doc)
            self.mocks['abort_mock'].assert_called_with(
                409, extra='error_message'
            )

    def test_validate_cpf_valid_returns_nothing(self):
        # Setup
        doc = {'cpf': '12345678912'}
        self.mocks['cpf_mock'].return_value.\
            validate.return_value = True

        # Act
        RegistrationService._validate_cpf(doc)

        # Assert
        self.mocks['cpf_mock'].return_value.\
            validate.assert_called_with(
                '12345678912'
            )

    def test_validate_cpf_invalid_abort(self):
        # Setup
        doc = {'cpf': '12345678912'}
        self.mocks['cpf_mock'].return_value.\
            validate.return_value = False
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            RegistrationService._validate_cpf(doc)
            self.mocks['abort_mock'].assert_called_with(
                400, extra='Invalid CPF'
            )

    def test_validate_cnpj_valid_returns_nothing(self):
        # Setup
        doc = {'cnpj': '12345678912'}
        self.mocks['cnpj_mock'].return_value.\
            validate.return_value = True

        # Act
        RegistrationService._validate_cnpj(doc)

        # Assert
        self.mocks['cnpj_mock'].return_value.\
            validate.assert_called_with(
                '12345678912'
            )

    def test_validate_cnpj_invalid_abort(self):
        # Setup
        doc = {'cnpj': '12345678912'}
        self.mocks['cnpj_mock'].return_value.\
            validate.return_value = False
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            RegistrationService._validate_cnpj(doc)
            self.mocks['abort_mock'].assert_called_with(
                400, extra='Invalid CNPJ'
            )

    def test_create_array_fields_type_client_create_pets_array(self):
        # Setup
        doc = {}
        type_ = 'client'

        # Act
        RegistrationService._create_array_fields(doc, type_)

        # Assert
        self.assertEqual(doc, {'pets': []})

    def test_create_array_fields_type_shop_create_services_array(self):
        # Setup
        doc = {}
        type_ = 'shop'

        # Act
        RegistrationService._create_array_fields(doc, type_)

        # Assert
        self.assertEqual(doc, {'services': []})
