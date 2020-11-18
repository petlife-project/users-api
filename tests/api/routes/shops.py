import unittest
from unittest.mock import patch

from users.api.routes.shops import Shops


class ShopsTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        resource_patch = patch('users.api.routes.shops.Resource')
        self.mocks['resource_mock'] = resource_patch.start()
        self.patches.append(resource_patch)

        registration_service_patch = patch('users.api.routes.shops.RegistrationService')
        self.mocks['registration_service_mock'] = registration_service_patch.start()
        self.patches.append(registration_service_patch)

        update_service_patch = patch('users.api.routes.shops.UpdateService')
        self.mocks['update_service_mock'] = update_service_patch.start()
        self.patches.append(update_service_patch)

        removal_service_patch = patch('users.api.routes.shops.RemovalService')
        self.mocks['removal_service_mock'] = removal_service_patch.start()
        self.patches.append(removal_service_patch)

        get_all_service_patch = patch('users.api.routes.shops.GetAllService')
        self.mocks['get_all_service_mock'] = get_all_service_patch.start()
        self.patches.append(get_all_service_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_post_calls_registration_service(self):
        # Act
        Shops.post()

        # Assert
        self.mocks['registration_service_mock'].assert_called()
        self.mocks['registration_service_mock'].return_value.\
            register.assert_called_with('shop')

    def test_put_calls_update_service(self):
        # Act
        Shops.put()

        # Assert
        self.mocks['update_service_mock'].assert_called()
        self.mocks['update_service_mock'].return_value.\
            update.assert_called_with('shop')

    def test_delete_calls_removal_service(self):
        # Act
        Shops.delete()

        # Assert
        self.mocks['removal_service_mock'].assert_called()
        self.mocks['removal_service_mock'].return_value.\
            remove.assert_called()

    def test_get_calls_get_all_service(self):
        # Act
        Shops.get()

        # Assert
        self.mocks['get_all_service_mock'].assert_called()
        self.mocks['get_all_service_mock'].return_value.\
            get.assert_called()
