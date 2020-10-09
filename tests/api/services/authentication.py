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

        jsonify_patch = patch('users.api.services.authentication.jsonify')
        self.mocks['jsonify_mock'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

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

    def test_authenticate_successful_returns_user(self):
        # Setup
        mock_self = MagicMock(collections={'client': 'test_col'})
        mock_self.parser.fields = {
            'username': 'dude',
            'password': 'hangloose',
            'type': 'client'
        }
        self.mocks['jsonify_mock'].return_value = {
            'username': 'dude'
        }

        # Act
        result = AuthenticationService.authenticate(mock_self)

        # Assert
        mock_self._get_from_mongo.assert_called_with(
            'test_col', {
                'username': 'dude',
                'password': 'hangloose'
            }
        )
        self.assertEqual(result, {
            'username': 'dude'
        })

    def test_get_from_mongo_return_user_object(self):
        # Setup
        collection = 'test_col'
        user = {
            'username': 'crying',
            'password': 'lighting'
        }
        self.mocks['mongo_mock'].return_value.get_user_information.\
            return_value = {
                'username': 'ape',
                'password': 'monke',
                'and': 'other',
                'fields': 'thats',
                'are': 'here'
            }

        # Act
        db_data = AuthenticationService.\
            _get_from_mongo(collection, user)

        # Assert
        self.mocks['mongo_mock'].return_value.get_user_information.\
            assert_called_with('test_col', 'crying', 'lighting')
        self.assertDictEqual(db_data, {
                'username': 'ape',
                'password': 'monke',
                'and': 'other',
                'fields': 'thats',
                'are': 'here'
        })

    def test_get_from_mongo_wrong_credentials(self):
        # Setup
        collection = 'test_col'
        user = {
            'username': 'you_shall',
            'password': 'not_PASS'
        }
        self.mocks['mongo_mock'].return_value.get_user_information.\
            side_effect = KeyError('SAI FORA MANO')
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            AuthenticationService._get_from_mongo(collection, user)
            self.mocks['abort_mock'].assert_called_with(
                401, extra='SAI FORA MANO'
            )
