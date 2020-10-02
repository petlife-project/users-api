import unittest
from unittest.mock import patch, MagicMock

from users.api.body_parsers.factory import BodyParserFactory


# pylint: disable=protected-access
class BodyParserFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        auth_patch = patch('users.api.body_parsers.factory.AuthParser')
        self.mocks['auth_mock'] = auth_patch.start()
        self.patches.append(auth_patch)

        client_reg_patch = patch('users.api.body_parsers.factory.ClientRegParser')
        self.mocks['client_reg_mock'] = client_reg_patch.start()
        self.patches.append(client_reg_patch)

        shop_reg_patch = patch('users.api.body_parsers.factory.ShopRegParser')
        self.mocks['shop_reg_mock'] = shop_reg_patch.start()
        self.patches.append(shop_reg_patch)

        client_update_patch = patch('users.api.body_parsers.factory.ClientUpdateParser')
        self.mocks['client_update_mock'] = client_update_patch.start()
        self.patches.append(client_update_patch)

        shop_update_patch = patch('users.api.body_parsers.factory.ShopUpdateParser')
        self.mocks['shop_update_mock'] = shop_update_patch.start()
        self.patches.append(shop_update_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_create_types_dict(self):
        # Setup
        mock_self = MagicMock()
        expected = {
            'auth': self.mocks['auth_mock'],
            'client_registration': self.mocks['client_reg_mock'],
            'shop_registration': self.mocks['shop_reg_mock'],
            'client_update': self.mocks['client_update_mock'],
            'shop_update': self.mocks['shop_update_mock']
        }

        # Act
        BodyParserFactory.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self.types, expected)

    def test_get_parser_return_instance_of_selected_parser(self):
        # Setup
        mock_self = MagicMock(types={
            'auth': self.mocks['auth_mock'],
            'client_registration': self.mocks['client_reg_mock'],
            'shop_registration': self.mocks['shop_reg_mock'],
            'client_update': self.mocks['client_update_mock'],
            'shop_update': self.mocks['shop_update_mock']
        })
        type_ = 'auth'

        # Act
        parser = BodyParserFactory.get_parser(mock_self, type_)

        # Assert
        self.assertEqual(parser, self.mocks['auth_mock'].return_value)
