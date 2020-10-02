import unittest
from unittest.mock import MagicMock, patch

from users.api.body_parsers.registration.clients import ClientRegParser, BaseRegParser


# pylint: disable=protected-access
class ClientRegistrationParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(ClientRegParser, BaseRegParser))

    def test_init_extends_add_fields(self):
        # Setup
        mock_self = MagicMock(_additional_fields=[])

        # Act
        with patch('users.api.body_parsers.registration.clients.super'):
            ClientRegParser.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self._additional_fields, [
            {'name': 'cpf', 'type': str, 'location': 'form', 'required': False}
        ])
