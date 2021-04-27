import unittest
from unittest.mock import patch, MagicMock

from users.api.body_parsers.factory import BodyParserFactory


# pylint: disable=protected-access
class BodyParserFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        parser_patch = patch('users.api.body_parsers.factory.BodyParser')
        self.mocks['parser'] = parser_patch.start()
        self.patches.append(parser_patch)

        auth_fields_patch = patch(
            'users.api.body_parsers.factory.AUTH_FIELDS', new='auth fields'
        )
        self.mocks['auth_fields'] = auth_fields_patch.start()
        self.patches.append(auth_fields_patch)

        clients_reg_fields_patch = patch(
            'users.api.body_parsers.factory.CLIENTS_REGISTRATION_FIELDS', new='client reg fields'
        )
        self.mocks['clients_reg_fields'] = clients_reg_fields_patch.start()
        self.patches.append(clients_reg_fields_patch)

        clients_up_fields_patch = patch(
            'users.api.body_parsers.factory.CLIENTS_UPDATE_FIELDS', new='client up fields'
        )
        self.mocks['clients_up_fields'] = clients_up_fields_patch.start()
        self.patches.append(clients_up_fields_patch)

        shops_reg_fields_patch = patch(
            'users.api.body_parsers.factory.SHOPS_REGISTRATION_FIELDS', new='shops reg fields'
        )
        self.mocks['shops_reg_fields'] = shops_reg_fields_patch.start()
        self.patches.append(shops_reg_fields_patch)

        shops_up_fields_patch = patch(
            'users.api.body_parsers.factory.SHOPS_UPDATE_FIELDS', new='shops up fields'
        )
        self.mocks['shops_up_fields'] = shops_up_fields_patch.start()
        self.patches.append(shops_up_fields_patch)

        service_rm_fields_patch = patch(
            'users.api.body_parsers.factory.SERVICE_REMOVAL', new='service rm fields'
        )
        self.mocks['service_rm_fields'] = service_rm_fields_patch.start()
        self.patches.append(service_rm_fields_patch)

        pet_rm_fields_patch = patch(
            'users.api.body_parsers.factory.PET_REMOVAL', new='pet rm fields'
        )
        self.mocks['pet_rm_fields'] = pet_rm_fields_patch.start()
        self.patches.append(pet_rm_fields_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_create_types_dict(self):
        # Setup
        mock_self = MagicMock()
        expected = {
            'auth': 'auth fields',
            'client_registration': 'client reg fields',
            'shop_registration': 'shops reg fields',
            'client_update': 'client up fields',
            'shop_update': 'shops up fields',
            'service_removal': 'service rm fields',
            'pet_removal': 'pet rm fields'
        }

        # Act
        BodyParserFactory.__init__(mock_self)

        # Assert
        self.assertEqual(mock_self.types, expected)

    def test_get_parser_return_instance_of_selected_parser(self):
        # Setup
        mock_self = MagicMock(types={
            'auth': self.mocks['auth_fields']
        })
        type_ = 'auth'

        # Act
        parser = BodyParserFactory.get_parser(mock_self, type_)

        # Assert
        self.mocks['parser'].assert_called_with(self.mocks['auth_fields'])
        self.assertEqual(parser, self.mocks['parser'].return_value)
