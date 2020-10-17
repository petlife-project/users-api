import unittest
from unittest.mock import MagicMock, patch

from users.api.body_parsers.update.base import BaseUpdateParser, BaseParser


# pylint: disable=protected-access
class BaseUpdateParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(BaseUpdateParser, BaseParser))

    def test_init_extends_add_fields(self):
        # Setup
        mock_self = MagicMock(_additional_fields=[])

        # Act
        with patch('users.api.body_parsers.update.base.super'):
            BaseUpdateParser.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self._additional_fields, [
            {'name': 'name', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False},
            {'name': 'email', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False},
            {'name': 'address', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False},
            {'name': 'phone_number', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False}
        ])
