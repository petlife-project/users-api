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

        parser_factory_patch = patch('users.api.services.registration.BodyParserFactory')
        self.mocks['parser_factory_mock'] = parser_factory_patch.start()
        self.patches.append(parser_factory_patch)

        mongo_patch = patch('users.api.services.registration.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        clients_col_patch = patch('users.api.services.registration.CLIENTS_COLLECTION',
                                  new='test_clients_col')
        self.mocks['clients_col_mock'] = clients_col_patch.start()
        self.patches.append(clients_col_patch)

        shops_col_patch = patch('users.api.services.registration.SHOPS_COLLECTION',
                                  new='test_shops_col')
        self.mocks['shops_col_mock'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_dict_and_parser_factory(self):
        # Setup
        mock_self = MagicMock(
            _register_client='function1',
            _register_shop='function2'
        )

        # Act
        RegistrationService.__init__(mock_self)

        # Assert
        self.assertDictEqual(mock_self.types,
            {'client': 'function1', 'shop': 'function2'}
        )
        mock_self.parser_factory = self.mocks['parser_factory_mock'].return_value

    @staticmethod
    def test_register_returns_chosen_type_call():
        # Setup
        registration_method = MagicMock()
        mock_self = MagicMock(types={'test_type': registration_method})
        type_ = 'test_type'

        # Act
        RegistrationService.register(mock_self, type_)

        # Assert
        registration_method.assert_called()

    def test_register_client_creates_user_with_cpf_returns_new_user(self):
        # Setup
        mock_self = MagicMock()
        mock_self.parser_factory.get_parser.return_value = MagicMock(
            fields={
                'username': 'user123',
                'cpf': '123'
            }
        )
        self.mocks['jsonify_mock'].return_value = {
            'ta': 'muito',
            'calor': 'mano'
        }

        # Act
        new_user = RegistrationService._register_client(mock_self)

        # Assert
        mock_self._validate_cpf.assert_called_with('123')
        mock_self._insert_in_mongo.assert_called_with(
            'test_clients_col', {
                'username': 'user123',
                'cpf': '123'
            }
        )
        self.mocks['jsonify_mock'].assert_called_with({
                'username': 'user123',
                'cpf': '123'
            })
        self.assertDictEqual(new_user, {
            'ta': 'muito',
            'calor': 'mano'
        })

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
        cpf = '12345678912'
        self.mocks['cpf_mock'].return_value.\
            validate.return_value = True

        # Act
        RegistrationService._validate_cpf(cpf)

        # Assert
        self.mocks['cpf_mock'].return_value.\
            validate.assert_called_with(
                '12345678912'
            )

    def test_validate_cpf_invalid_abort(self):
        # Setup
        cpf = '12345678912'
        self.mocks['cpf_mock'].return_value.\
            validate.return_value = False
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            RegistrationService._validate_cpf(cpf)
            self.mocks['abort_mock'].assert_called_with(
                400, extra='Invalid CPF'
            )

    def test_register_shop_creates_client_returns_new_client(self):
        # Setup
        mock_self = MagicMock()
        mock_self.parser_factory.get_parser.return_value = MagicMock(
            fields={
                'username': 'user123',
                'cnpj': 'cnpj123'
            }
        )
        self.mocks['jsonify_mock'].return_value = {
            'hoje': 'ja',
            'nao': 'ta',
            'tanto': 'calor'
        }

        # Act
        new_shop = RegistrationService._register_shop(mock_self)

        # Assert
        mock_self._validate_cnpj.assert_called_with('cnpj123')
        mock_self._insert_in_mongo.assert_called_with(
            'test_shops_col', {
                'username': 'user123',
                'cnpj': 'cnpj123'
            }
        )
        self.assertDictEqual(new_shop, {
            'hoje': 'ja',
            'nao': 'ta',
            'tanto': 'calor'
            }
        )

    def test_validate_cnpj_valid_returns_nothing(self):
        # Setup
        cnpj = '12345678912'
        self.mocks['cnpj_mock'].return_value.\
            validate.return_value = True

        # Act
        RegistrationService._validate_cnpj(cnpj)

        # Assert
        self.mocks['cnpj_mock'].return_value.\
            validate.assert_called_with(
                '12345678912'
            )

    def test_validate_cnpj_invalid_abort(self):
        # Setup
        cnpj = '12345678912'
        self.mocks['cnpj_mock'].return_value.\
            validate.return_value = False
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            RegistrationService._validate_cnpj(cnpj)
            self.mocks['abort_mock'].assert_called_with(
                400, extra='Invalid CNPJ'
            )
