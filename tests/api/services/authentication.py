import unittest
from unittest.mock import MagicMock, patch

from werkzeug.exceptions import HTTPException

from users.api.services.authentication import AuthenticationService


# pylint: disable=protected-access
class AuthenticationServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.authentication.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        parser_factory_patch = patch('users.api.services.authentication.FACTORY')
        self.mocks['parser_factory_mock'] = parser_factory_patch.start()
        self.patches.append(parser_factory_patch)

        mongo_patch = patch('users.api.services.authentication.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        clients_col_patch = patch('users.api.services.authentication.CLIENTS_COLLECTION',
                                  new='test_clients_col')
        self.mocks['clients_col_mock'] = clients_col_patch.start()
        self.patches.append(clients_col_patch)

        shops_col_patch = patch('users.api.services.authentication.SHOPS_COLLECTION',
                                  new='test_shops_col')
        self.mocks['shops_col_mock'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_col_dict_and_parser(self):
        # Setup
        mock_self = MagicMock()

        # Act
        AuthenticationService.__init__(mock_self)

        # Assert
        self.assertDictEqual(
            mock_self.collections, {
            'client': self.mocks['clients_col_mock'],
            'shop': self.mocks['shops_col_mock']
            }
        )
        self.mocks['parser_factory_mock'].get_parser.assert_called_with('auth')

    def test_authenticate_successful_returns_200(self):
        # Setup
        mock_self = MagicMock(collections={'client': 'test_col'})
        mock_self.parser.fields = {
            'username': 'dude',
            'type': 'client'
        }
        mock_self._get_from_mongo.return_value = 'db_data'

        # Act
        result = AuthenticationService.authenticate(mock_self)

        # Assert
        mock_self._get_from_mongo.assert_called_with(
            'test_col', 'dude'
        )
        mock_self._validate_request_data.assert_called_with(
            {'username': 'dude'}, 'db_data'
        )
        self.assertEqual(result, 200)

    def test_get_from_mongo_gets_only_necessary_fields(self):
        # Setup
        collection = 'test_col'
        username = 'some_user'
        self.mocks['mongo_mock'].return_value.get_user_information.\
            return_value = {
                'username': 'ape',
                'password': 'monke',
                'and': 'other',
                'fields': 'thats',
                'will': 'not',
                'get': 'compared'
            }

        # Act
        info_to_compare = AuthenticationService.\
            _get_from_mongo(collection, username)

        # Assert
        self.mocks['mongo_mock'].return_value.get_user_information.\
            assert_called_with('test_col', 'some_user')
        self.assertDictEqual(info_to_compare, {
            'username': 'ape',
            'password': 'monke'
        })

    def test_validate_request_data_valid(self):
        # Setup
        request_data = {'fields': 'should', 'be': 'equal'}
        db_data = {'fields': 'should', 'be': 'equal'}

        # Act
        AuthenticationService._validate_request_data(
            request_data, db_data
        )

        # Assert
        self.mocks['abort_mock'].assert_not_called()

    def test_validate_request_data_invalid(self):
        # Setup
        request_data = {'fields': 'should', 'be': 'equal'}
        db_data = {'fields': 'should', 'be': 'unequal'}
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            AuthenticationService._validate_request_data(
                request_data, db_data
            )
            self.mocks['abort_mock'].assert_called_with(
                401, extra='Invalid username or password'
            )
