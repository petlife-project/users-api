import unittest
from unittest.mock import patch

from users.api.services.get_all import GetAllService


# pylint: disable=protected-access
class GetAllServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        abort_patch = patch('users.api.services.get_all.abort')
        self.mocks['abort'] = abort_patch.start()
        self.patches.append(abort_patch)

        mongo_patch = patch('users.api.services.get_all.get_mongo_adapter')
        self.mocks['mongo'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        shops_col_patch = patch('users.api.services.get_all.SHOPS_COLLECTION',
                                new='test_shops_col')
        self.mocks['shops_col'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_get_returns_mongo_return(self):
        # Act
        response = GetAllService.get()

        # Assert
        self.assertEqual(
            response,
            self.mocks['mongo'].return_value.get_users.return_value
        )

    def test_get_keyerro_aborts_404(self):
        # Setup
        self.mocks['mongo'].return_value.get_users.side_effect = KeyError

        # Act
        GetAllService.get()

        # Assert
        self.mocks['abort'].assert_called()
