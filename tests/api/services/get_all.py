import unittest
from unittest.mock import patch, MagicMock

from users.api.services.get_all import GetAllService


# pylint: disable= (protected-access)
class GetAllServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.get_all.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        mongo_patch = patch('users.api.services.get_all.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        shops_col_patch = patch('users.api.services.get_all.SHOPS_COLLECTION',
                                  new='test_shops_col')
        self.mocks['shops_col_mock'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_get_calls_mongo_method_returns_shops_list(self):
        # Arrange
        mock_self = MagicMock()

        # Act
        response = GetAllService.get(mock_self)

        # Assert
        self.assertEqual(
            response,
            mock_self._get_from_mongo.return_value
        )

    def test_get_from_mongo_successful_returns_list(self):
        # Act
        results = GetAllService._get_from_mongo()

        # Assert
        self.mocks['mongo_mock'].return_value.get_users.assert_called_with(
           'test_shops_col'
        )
        self.assertEqual(
            results,
            self.mocks['mongo_mock'].return_value.get_users.return_value
        )

    def test_get_from_mongo_malformed_data_calls_abort(self):
        # Arrange
        self.mocks['mongo_mock'].return_value.get_users.side_effect = KeyError('pao de batata')

        # Act
        GetAllService._get_from_mongo()

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            500, extra="'pao de batata'"
        )
