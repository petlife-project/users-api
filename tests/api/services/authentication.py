import unittest
from unittest.mock import MagicMock, patch

from users.api.services.authentication import AuthenticationService


# pylint: disable=protected-access
class AuthenticationServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.authentication.abort')
        self.mocks['abort'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('users.api.services.authentication.jsonify')
        self.mocks['jsonify'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        get_jwt_identity_patch = patch('users.api.services.authentication.create_access_token')
        self.mocks['create_access_token'] = get_jwt_identity_patch.start()
        self.patches.append(get_jwt_identity_patch)

        get_jwt_identity_patch = patch('users.api.services.authentication.get_jwt_identity')
        self.mocks['get_jwt_identity'] = get_jwt_identity_patch.start()
        self.patches.append(get_jwt_identity_patch)

        parser_factory_patch = patch('users.api.services.authentication.FACTORY')
        self.mocks['parser_factory'] = parser_factory_patch.start()
        self.patches.append(parser_factory_patch)

        mongo_patch = patch('users.api.services.authentication.get_mongo_adapter')
        self.mocks['mongo'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        clients_col_patch = patch('users.api.services.authentication.CLIENTS_COLLECTION',
                                  new='test_clients_col')
        self.mocks['clients_col'] = clients_col_patch.start()
        self.patches.append(clients_col_patch)

        shops_col_patch = patch('users.api.services.authentication.SHOPS_COLLECTION',
                                new='test_shops_col')
        self.mocks['shops_col'] = shops_col_patch.start()
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
                'client': self.mocks['clients_col'],
                'shop': self.mocks['shops_col']
            }
        )
        self.mocks['parser_factory'].get_parser.assert_called_with('auth')

    def test_authenticate_successful_returns_user(self):
        # Setup
        mock_self = MagicMock(collections={'client': 'test_col'})
        mock_self.parser.fields = {
            'username': 'dude',
            'password': 'hangloose',
            'type': 'client'
        }

        # Act
        AuthenticationService.authenticate(mock_self)

        # Assert
        self.mocks['mongo'].return_value.get_user_by_username.assert_called_with(
            'test_col', 'dude', 'hangloose'
        )
        self.mocks['jsonify'].assert_called_with(
            self.mocks['create_access_token'].return_value
        )

    def test_authenticate_keyerror_abort(self):
        # Setup
        mock_self = MagicMock()
        self.mocks['mongo'].return_value.get_user_by_username.side_effect = KeyError

        # Act
        AuthenticationService.authenticate(mock_self)

        # Assert
        self.mocks['abort'].assert_called()

    def test_delete_user_deletes_user_on_db(self):
        # Setup
        mock_self = MagicMock(collections={'client': 'test_col'})
        self.mocks['get_jwt_identity'].return_value = {
            'type': 'client',
            '_id': 'test_id'
        }

        # Act
        AuthenticationService.delete_user(mock_self)

        # Assert
        self.mocks['mongo'].return_value.delete.assert_called_with(
            'test_col', 'test_id'
        )
