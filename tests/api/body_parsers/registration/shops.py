import unittest
from unittest.mock import MagicMock, patch

from users.api.body_parsers.registration.shops import ShopRegParser, BaseRegParser


# pylint: disable=protected-access
class ClientUpdateParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(ShopRegParser, BaseRegParser))

    def test_init_extends_add_fields(self):
        # Setup
        mock_self = MagicMock(_additional_fields=[])

        # Act
        with patch('users.api.body_parsers.registration.shops.super'):
            ShopRegParser.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self._additional_fields, [
            {'name': 'cnpj', 'type': str, 'location': 'form', 'required': True}
        ])
