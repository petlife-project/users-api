import unittest
from unittest.mock import patch

from users.api.routes.auth import Auth


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        resource_patch = patch('users.api.routes.auth.Resource')
        self.mocks['resource_mock'] = resource_patch.start()
        self.patches.append(resource_patch)

        auth_service_patch = patch('users.api.routes.auth.AuthenticationService')
        self.mocks['auth_service_mock'] = auth_service_patch.start()
        self.patches.append(auth_service_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_post_calls_authentication_service(self):
        # Act
        Auth.post()

        # Assert
        self.mocks['auth_service_mock'].assert_called()
        self.mocks['auth_service_mock'].return_value.\
            authenticate.assert_called()
