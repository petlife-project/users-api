import unittest
from unittest.mock import MagicMock, patch

from users.api.services.removal import RemovalService


# pylint: disable=protected-access
class RemovalServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.removal.abort')
        self.mocks['abort'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('users.api.services.removal.jsonify')
        self.mocks['jsonify'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        get_jwt_id_patch = patch('users.api.services.removal.get_jwt_identity')
        self.mocks['get_jwt_id'] = get_jwt_id_patch.start()
        self.patches.append(get_jwt_id_patch)

        mongo_patch = patch('users.api.services.removal.get_mongo_adapter')
        self.mocks['mongo'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        parser_factory_patch = patch('users.api.services.removal.FACTORY')
        self.mocks['parser_factory'] = parser_factory_patch.start()
        self.patches.append(parser_factory_patch)

        shops_col_patch = patch('users.api.services.removal.SHOPS_COLLECTION',
                                new='test_shops_col')
        self.mocks['shops_col'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

        clients_col_patch = patch('users.api.services.removal.CLIENTS_COLLECTION',
                                  new='test_clients_col')
        self.mocks['clients_col'] = clients_col_patch.start()
        self.patches.append(clients_col_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_sets_factory_and_maps(self):
        # Setup
        mock_self = MagicMock()

        # Act
        RemovalService.__init__(mock_self)

        # Assert
        self.assertEqual(
            mock_self.parser_factory,
            self.mocks['parser_factory']
        )
        self.assertEqual(
            mock_self.collections,
            {'client': 'test_clients_col', 'shop': 'test_shops_col'}
        )
        self.assertEqual(
            mock_self.parser_type,
            {'client': 'pet_removal', 'shop': 'service_removal'}
        )

    def test_remove_succesful_returns_updated_user(self):
        # Setup
        mock_self = MagicMock(collections={'type': 'test_type'})
        type_ = 'type'

        # Act
        updated = RemovalService.remove(mock_self, type_)

        # Assert
        self.mocks['jsonify'].assert_called_with(
            self.mocks['mongo'].return_value.remove.return_value
        )
        self.assertEqual(updated, self.mocks['jsonify'].return_value)

    def test_remove_key_error_abort_404(self):
        # Setup
        mock_self = MagicMock(collections={'type': 'test_type'})
        type_ = 'type'
        self.mocks['mongo'].return_value.remove.side_effect = KeyError

        # Act
        RemovalService.remove(mock_self, type_)

        # Assert
        self.mocks['abort'].assert_called_with(404)
        self.mocks['jsonify'].assert_not_called()

    def test_remove_runtime_error_abort_500(self):
        # Setup
        mock_self = MagicMock(collections={'type': 'test_type'})
        type_ = 'type'
        self.mocks['mongo'].return_value.remove.side_effect = RuntimeError(';(')

        # Act
        RemovalService.remove(mock_self, type_)

        # Assert
        self.mocks['abort'].assert_called_with(500, extra='Error when updating, ;(')
        self.mocks['jsonify'].assert_not_called()
