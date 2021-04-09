import unittest
from unittest.mock import MagicMock, patch

from werkzeug.exceptions import HTTPException

from users.api.services.removal import RemovalService


# pylint: disable=protected-access
class RemovalServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.removal.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('users.api.services.removal.jsonify')
        self.mocks['jsonify_mock'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        mongo_patch = patch('users.api.services.removal.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        parser_factory_patch = patch('users.api.services.removal.FACTORY')
        self.mocks['parser_factory_mock'] = parser_factory_patch.start()
        self.patches.append(parser_factory_patch)

        shops_col_patch = patch('users.api.services.removal.SHOPS_COLLECTION',
                                new='test_shops_col')
        self.mocks['shops_col_mock'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_gets_parser_from_factory(self):
        # Setup
        mock_self = MagicMock()

        # Act
        RemovalService.__init__(mock_self)

        # Assert
        self.assertEqual(
            mock_self.parser,
            self.mocks['parser_factory_mock'].get_parser.return_value
        )

    def test_remove_succesful_returns_updated_user(self):
        # Setup
        mock_self = MagicMock()

        # Act
        updated = RemovalService.remove(mock_self)

        # Assert
        self.mocks['jsonify_mock'].assert_called_with(
            mock_self._update_in_mongo.return_value
        )
        self.assertEqual(updated, self.mocks['jsonify_mock'].return_value)

    def test_update_in_mongo_successful_returns_updated(self):
        # Setup
        collection = 'test_col'
        doc = {'test': 'doc'}

        # Act
        RemovalService._update_in_mongo(collection, doc)

        # Assert
        self.mocks['mongo_mock'].return_value.remove_service.assert_called_with(
            'test_col', {'test': 'doc'}
        )

    def test_update_in_mongo_incorrect_credentials(self):
        # Setup
        collection = 'test_col'
        doc = {}
        self.mocks['mongo_mock'].return_value.remove_service.side_effect = \
            KeyError
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            RemovalService._update_in_mongo(collection, doc)
            self.mocks['abort_mock'].assert_called_with(
                400, extra='Incorrect username or password.'
            )

    def test_update_in_mongo_unexpected_error(self):
        # Setup
        collection = 'test_col'
        doc = {}
        self.mocks['mongo_mock'].return_value.remove_service.side_effect = \
            RuntimeError('deu ruim')
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            RemovalService._update_in_mongo(collection, doc)
            self.mocks['abort_mock'].assert_called_with(
                500, extra='Error when updating, deu ruim'
            )
