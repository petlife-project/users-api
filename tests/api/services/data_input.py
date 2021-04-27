import unittest
from unittest.mock import MagicMock, patch, call

from werkzeug.exceptions import HTTPException

from users.api.services.data_input import DataInputService


# pylint: disable=protected-access
class DataInputServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        re_patch = patch('users.api.services.data_input.re')
        self.mocks['re'] = re_patch.start()
        self.patches.append(re_patch)

        abort_patch = patch('users.api.services.data_input.abort')
        self.mocks['abort'] = abort_patch.start()
        self.patches.append(abort_patch)

        get_jwt_id_patch = patch('users.api.services.data_input.get_jwt_identity')
        self.mocks['get_jwt_id'] = get_jwt_id_patch.start()
        self.patches.append(get_jwt_id_patch)

        parser_factory_patch = patch('users.api.services.data_input.FACTORY')
        self.mocks['parser_factory'] = parser_factory_patch.start()
        self.patches.append(parser_factory_patch)

        clients_col_patch = patch('users.api.services.data_input.CLIENTS_COLLECTION',
                                  new='test_clients_col')
        self.mocks['clients_col'] = clients_col_patch.start()
        self.patches.append(clients_col_patch)

        shops_col_patch = patch('users.api.services.data_input.SHOPS_COLLECTION',
                                new='test_shops_col')
        self.mocks['shops_col'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

        jsonify_patch = patch('users.api.services.data_input.jsonify')
        self.mocks['jsonify'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        cpf_patch = patch('users.api.services.data_input.CPF')
        self.mocks['cpf'] = cpf_patch.start()
        self.patches.append(cpf_patch)

        cnpj_patch = patch('users.api.services.data_input.CNPJ')
        self.mocks['cnpj'] = cnpj_patch.start()
        self.patches.append(cnpj_patch)

        mongo_patch = patch('users.api.services.data_input.get_mongo_adapter')
        self.mocks['mongo'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        cos_patch = patch('users.api.services.data_input.get_cos_adapter')
        self.mocks['cos'] = cos_patch.start()
        self.patches.append(cos_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_sets_factory_types_and_validations(self):
        # Setup
        mock_self = MagicMock(
            _validate_email='method1',
            _validate_pics='method4',
            _validate_cpf='method5',
            _validate_cnpj='method6'
        )

        # Act
        DataInputService.__init__(mock_self)

        # Assert
        self.assertEqual(
            mock_self.parser_factory,
            self.mocks['parser_factory']
        )
        self.assertEqual(
            mock_self.types,
            {
                'client': 'test_clients_col',
                'shop': 'test_shops_col'
            }
        )
        self.assertDictEqual(
            mock_self.validations,
            {
                'email': 'method1',
                'cpf': 'method5',
                'cnpj': 'method6',
                'profile_pic': 'method4',
                'banner_pic': 'method4'
            }
        )

    def test_register_returns_new_user(self):
        # Setup
        new_user = {'new': 'user', 'right': 'here'}
        mock_self = MagicMock(types={'test_type': 'test_col'})
        mock_self.parser_factory.get_parser.return_value = \
            MagicMock(fields=new_user)
        type_ = 'test_type'

        # Act
        DataInputService.register(mock_self, type_)

        # Assert
        mock_self._validate_fields.assert_called_with(new_user)
        mock_self._create_array_fields.assert_called_with(
            new_user, 'test_type'
        )
        self.mocks['mongo'].return_value.create.assert_called_with(
            'test_col', new_user
        )
        self.mocks['jsonify'].assert_called()

    def test_register_keyerror_abort(self):
        # Setup
        new_user = {'new': 'user', 'right': 'here'}
        mock_self = MagicMock(types={'test_type': 'test_col'})
        mock_self.parser_factory.get_parser.return_value = \
            MagicMock(fields=new_user)
        type_ = 'test_type'
        self.mocks['mongo'].return_value.create.side_effect = \
            KeyError

        # Act
        DataInputService.register(mock_self, type_)

        # Assert
        mock_self._validate_fields.assert_called_with(new_user)
        mock_self._create_array_fields.assert_called_with(
            new_user, 'test_type'
        )
        self.mocks['abort'].assert_called()

    def test_update_succesful_returns_updated_user(self):
        # Setup
        mock_self = MagicMock(types={'sftd': 'test_col'})
        type_ = 'sftd'
        mock_self.parser_factory.get_parser.return_value = \
            MagicMock(fields={'purple': 'haze'})
        self.mocks['get_jwt_id'].return_value = {'_id': 'mano'}

        # Act
        updated = DataInputService.update(mock_self, type_)

        # Assert
        mock_self.parser_factory.get_parser.assert_called_with(
            'sftd_update'
        )
        self.mocks['mongo'].return_value.update.assert_called_with(
            'test_col', {'purple': 'haze'}, 'mano'
        )
        self.assertEqual(updated, self.mocks['jsonify'].return_value)

    def test_update_key_error_abort_404(self):
        # Setup
        mock_self = MagicMock(types={'sftd': 'test_col'})
        type_ = 'sftd'
        self.mocks['mongo'].return_value.update.side_effect = KeyError(123)

        # Act
        DataInputService.update(mock_self, type_)

        # Assert
        self.mocks['abort'].assert_called_with(404, extra='123')

    def test_update_runtime_error_abort_500(self):
        # Setup
        mock_self = MagicMock(types={'sftd': 'test_col'})
        type_ = 'sftd'
        self.mocks['mongo'].return_value.update.side_effect = RuntimeError('=[')

        # Act
        DataInputService.update(mock_self, type_)

        # Assert
        self.mocks['abort'].assert_called_with(500, extra='Error when updating, =[')

    def test_validate_pics_creates_pics_object_inserts_pics(self):
        # Setup
        doc = {
            'profile_pic': 'fotos_da_festa.exe',
            'banner_pic': 'nao_eh_virus.exe'
        }

        # Act
        DataInputService._validate_pics(doc)

        # Assert
        self.mocks['cos'].return_value.upload.assert_has_calls(
            (call('fotos_da_festa.exe'), call('nao_eh_virus.exe'))
        )

    def test_validate_cpf_valid_returns_nothing(self):
        # Setup
        doc = {'cpf': '12345678912'}
        self.mocks['cpf'].return_value.\
            validate.return_value = True

        # Act
        DataInputService._validate_cpf(doc)

        # Assert
        self.mocks['cpf'].return_value.\
            validate.assert_called_with(
                '12345678912'
            )

    def test_validate_cpf_invalid_abort(self):
        # Setup
        doc = {'cpf': '12345678912'}
        self.mocks['cpf'].return_value.\
            validate.return_value = False
        self.mocks['abort'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            DataInputService._validate_cpf(doc)
            self.mocks['abort'].assert_called_with(
                400, extra='Invalid CPF'
            )

    def test_validate_cnpj_valid_returns_nothing(self):
        # Setup
        doc = {'cnpj': '12345678912'}
        self.mocks['cnpj'].return_value.\
            validate.return_value = True

        # Act
        DataInputService._validate_cnpj(doc)

        # Assert
        self.mocks['cnpj'].return_value.\
            validate.assert_called_with(
                '12345678912'
            )

    def test_validate_cnpj_invalid_abort(self):
        # Setup
        doc = {'cnpj': '12345678912'}
        self.mocks['cnpj'].return_value.\
            validate.return_value = False
        self.mocks['abort'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            DataInputService._validate_cnpj(doc)
            self.mocks['abort'].assert_called_with(
                400, extra='Invalid CNPJ'
            )

    def test_create_array_fields_type_client_create_pets_array(self):
        # Setup
        doc = {}
        type_ = 'client'

        # Act
        DataInputService._create_array_fields(doc, type_)

        # Assert
        self.assertEqual(doc, {'pets': []})

    def test_create_array_fields_type_shop_create_services_array(self):
        # Setup
        doc = {}
        type_ = 'shop'

        # Act
        DataInputService._create_array_fields(doc, type_)

        # Assert
        self.assertEqual(doc, {'services': []})
    def test_validate_email_good_no_action(self):
        # Setup
        doc = {'email': 'holly@la.ca'}

        # Act
        DataInputService._validate_email(doc)

        # Assert
        self.mocks['re'].match.assert_called_with(
            r'\S+@\S+\.\S+', 'holly@la.ca'
        )
        self.mocks['abort'].assert_not_called()

    def test_validate_email_bad_abort(self):
        # Setup
        doc = {'email': 'bademail@badserver >('}
        self.mocks['re'].match.return_value = False
        self.mocks['abort'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            DataInputService._validate_email(doc)

    @staticmethod
    def test_validate_fields_run_validations():
        # Setup
        mock_self = MagicMock()
        mock_self.method = MagicMock(return_value=1)
        mock_self.validations = {
            'lol': mock_self.method
        }
        doc = {
            'billion': 'laughs',
            'lol': 'lol'
        }

        # Act
        DataInputService._validate_fields(mock_self, doc)

        # Assert
        mock_self.method.assert_called_once()
