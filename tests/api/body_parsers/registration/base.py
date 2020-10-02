import unittest
from unittest.mock import MagicMock, patch

from users.api.body_parsers.registration.base import BaseRegParser, BaseParser


# pylint: disable=protected-access
class BaseRegistrationParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(BaseRegParser, BaseParser))

    def test_init_extends_add_fields(self):
        # Setup
        mock_self = MagicMock(_additional_fields=[])

        # Act
        with patch('users.api.body_parsers.registration.base.super'):
            BaseRegParser.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self._additional_fields, [
            {'name': 'name', 'type': str, 'location': 'form', 'required': True},
            {'name': 'email', 'type': str, 'location': 'form', 'required': True},
            {'name': 'address', 'type': str, 'location': 'form', 'required': True},
            {'name': 'phone_number', 'type': str, 'location': 'form', 'required': True}
        ])
