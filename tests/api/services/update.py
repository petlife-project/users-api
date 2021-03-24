import unittest
from unittest.mock import MagicMock, call, patch

from werkzeug.exceptions import HTTPException

from users.api.services.update import UpdateService


# pylint: disable=protected-access
class UpdateServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.update.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('users.api.services.update.jsonify')
        self.mocks['jsonify_mock'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        mongo_patch = patch('users.api.services.update.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        cos_patch = patch('users.api.services.update.get_cos_adapter')
        self.mocks['cos_mock'] = cos_patch.start()
        self.patches.append(cos_patch)

        data_input_patch = patch('users.api.services.update.DataInputService')
        self.mocks['data_input_mock'] = data_input_patch.start()
        self.patches.append(data_input_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_sets_validations(self):
        # Setup
        mock_self = MagicMock(
            _validate_email='method1',
            _validate_pets='method2',
            _validate_services='method3',
            _validate_pics='method4'
        )

        # Act
        UpdateService.__init__(mock_self)

        # Assert
        self.assertDictEqual(mock_self.validations, {
            'email': 'method1',
            'profile_pic': 'method4',
            'banner_pic': 'method4'
        }
        )

    def test_update_succesful_returns_updated_user(self):
        # Setup
        mock_self = MagicMock(types={'sftd': 'test_col'})
        type_ = 'sftd'
        mock_self.parser_factory.get_parser.return_value = \
            MagicMock(fields={'purple': 'haze'})

        # Act
        updated = UpdateService.update(mock_self, type_)

        # Assert
        mock_self.parser_factory.get_parser.assert_called_with(
            'sftd_update'
        )
        mock_self._update_in_mongo.assert_called_with(
            'test_col', {'purple': 'haze'}
        )
        self.assertEqual(updated, self.mocks['jsonify_mock'].return_value)

    def test_update_in_mongo_successful_returns_updated(self):
        # Setup
        collection = 'test_col'
        doc = {'test': 'doc'}

        # Act
        UpdateService._update_in_mongo(collection, doc)

        # Assert
        self.mocks['mongo_mock'].return_value.update.assert_called_with(
            'test_col', {'test': 'doc'}
        )

    def test_update_in_mongo_incorrect_credentials(self):
        # Setup
        collection = 'test_col'
        doc = {}
        self.mocks['mongo_mock'].return_value.update.side_effect = \
            KeyError
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            UpdateService._update_in_mongo(collection, doc)
            self.mocks['abort_mock'].assert_called_with(
                400, extra='Incorrect username or password.'
            )

    def test_update_in_mongo_unexpected_error(self):
        # Setup
        collection = 'test_col'
        doc = {}
        self.mocks['mongo_mock'].return_value.update.side_effect = \
            RuntimeError('deu ruim')
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            UpdateService._update_in_mongo(collection, doc)
            self.mocks['abort_mock'].assert_called_with(
                500, extra='Error when updating, deu ruim'
            )

    def test_validate_pics_creates_pics_object_inserts_pics(self):
        # Setup
        doc = {
            'profile_pic': 'fotos_da_festa.exe',
            'banner_pic': 'nao_eh_virus.exe'
        }

        # Act
        UpdateService._validate_pics(doc)

        # Assert
        self.mocks['cos_mock'].return_value.upload.assert_has_calls(
            (call('fotos_da_festa.exe'), call('nao_eh_virus.exe'))
        )
