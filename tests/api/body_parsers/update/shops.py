import unittest
from unittest.mock import MagicMock, patch

from users.api.body_parsers.update.shops import ShopUpdateParser, BaseUpdateParser, FileStorage


# pylint: disable=protected-access
class ShopUpdateParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(ShopUpdateParser, BaseUpdateParser))

    def test_init_extends_add_fields(self):
        # Setup
        mock_self = MagicMock(_additional_fields=[])

        # Act
        with patch('users.api.body_parsers.update.shops.super'):
            ShopUpdateParser.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self._additional_fields, [
            {'name': 'services', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False},
            {'name': 'description', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False},
            {'name': 'hours', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False},
            {'name': 'profile_pic', 'type': FileStorage,
                'location': 'files', 'required': False, 'store_missing': False},
            {'name': 'banner_pic', 'type': FileStorage,
                'location': 'files', 'required': False, 'store_missing': False}
        ])
