import unittest
from unittest.mock import MagicMock, patch

from users.api.body_parsers.auth import AuthParser, BaseParser


# pylint: disable=protected-access
class AuthParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(AuthParser, BaseParser))

    def test_init_extends_add_fields(self):
        # Setup
        mock_self = MagicMock(_additional_fields=[])

        # Act
        with patch('users.api.body_parsers.auth.super'):
            AuthParser.__init__(mock_self)

        # Assert
        self.assertListEqual(
            mock_self._additional_fields,
            [{'name': 'type', 'type': str, 'location': 'form', 'required': True,
             'choices': ['client', 'shop']}]
        )
