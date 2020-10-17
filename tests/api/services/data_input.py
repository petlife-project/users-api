import unittest
from unittest.mock import MagicMock, patch

from werkzeug.exceptions import HTTPException

from users.api.services.data_input import DataInputService


# pylint: disable=protected-access
class DataInputServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = {}
        self.patches = []

        re_patch = patch('users.api.services.data_input.re')
        self.mocks['re_mock'] = re_patch.start()
        self.patches.append(re_patch)

        abort_patch = patch('users.api.services.data_input.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        parser_factory_patch = patch('users.api.services.data_input.FACTORY')
        self.mocks['parser_factory_mock'] = parser_factory_patch.start()
        self.patches.append(parser_factory_patch)

        clients_col_patch = patch('users.api.services.data_input.CLIENTS_COLLECTION',
                                  new='test_clients_col')
        self.mocks['clients_col_mock'] = clients_col_patch.start()
        self.patches.append(clients_col_patch)

        shops_col_patch = patch('users.api.services.data_input.SHOPS_COLLECTION',
                                  new='test_shops_col')
        self.mocks['shops_col_mock'] = shops_col_patch.start()
        self.patches.append(shops_col_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_validate_email_good_no_action(self):
        # Setup
        doc = {'email': 'holly@la.ca'}

        # Act
        DataInputService._validate_email(doc)

        # Assert
        self.mocks['re_mock'].match.assert_called_with(
            r'\S+@\S+\.\S+', 'holly@la.ca'
        )
        self.mocks['abort_mock'].assert_not_called()

    def test_validate_email_bad_abort(self):
        # Setup
        doc = {'email': 'bademail@badserver >('}
        self.mocks['re_mock'].match.return_value = False
        self.mocks['abort_mock'].side_effect = HTTPException

        # Act & Assert
        with self.assertRaises(HTTPException):
            DataInputService._validate_email(doc)

    @staticmethod
    def test_validate_fields_run_validations():
        # Setup
        mock_self = MagicMock()
        mock_self.method = MagicMock(return_value=1)
        mock_self.validations = {
            'lol': mock_self.method
        }
        doc = {
            'billion': 'laughs',
            'lol': 'lol'
        }

        # Act
        DataInputService._validate_fields(mock_self, doc)

        # Assert
        mock_self.method.assert_called_once()
