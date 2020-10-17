import unittest
from unittest.mock import MagicMock, patch

from users.api.body_parsers.update.clients import BaseUpdateParser, ClientUpdateParser


# pylint: disable=protected-access
class ClientUpdateParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(ClientUpdateParser, BaseUpdateParser))

    def test_init_extends_add_fields(self):
        # Setup
        mock_self = MagicMock(_additional_fields=[])

        # Act
        with patch('users.api.body_parsers.update.clients.super'):
            ClientUpdateParser.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self._additional_fields, [
            {'name': 'pets', 'type': str,
                'location': 'form', 'required': False, 'store_missing': False}
        ])
