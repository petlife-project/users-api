import unittest
from unittest.mock import patch

from users.api.routes.clients import Clients


class ClientsTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        resource_patch = patch('users.api.routes.clients.Resource')
        self.mocks['resource_mock'] = resource_patch.start()
        self.patches.append(resource_patch)

        registration_service_patch = patch('users.api.routes.clients.RegistrationService')
        self.mocks['registration_service_mock'] = registration_service_patch.start()
        self.patches.append(registration_service_patch)

        update_service_patch = patch('users.api.routes.clients.UpdateService')
        self.mocks['update_service_mock'] = update_service_patch.start()
        self.patches.append(update_service_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_post_calls_registration_service(self):
        # Act
        Clients.post()

        # Assert
        self.mocks['registration_service_mock'].assert_called()
        self.mocks['registration_service_mock'].return_value.\
            register.assert_called_with('client')

    def test_put_calls_update_service(self):
        # Act
        Clients.put()

        # Assert
        self.mocks['update_service_mock'].assert_called()
        self.mocks['update_service_mock'].return_value.\
            update.assert_called_with('client')
