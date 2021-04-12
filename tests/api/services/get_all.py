import unittest
from unittest.mock import patch

from users.api.services.get_all import GetAllService


# pylint: disable=protected-access
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
        # Act
        response = GetAllService.get()

        # Assert
        self.assertEqual(
            response,
            {}
        )
