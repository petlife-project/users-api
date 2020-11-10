import unittest
from unittest.mock import call, patch, MagicMock

from users.api.body_parsers.parser import BodyParser


# pylint: disable=protected-access
class BodyParserTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        flask_parser_patch = patch('users.api.body_parsers.parser.RequestParser')
        self.mocks['flask_parser_mock'] = flask_parser_patch.start()
        self.patches.append(flask_parser_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_calls_create_parser_and_parse_args(self):
        # Setup
        mock_self = MagicMock()
        fields = []

        # Act
        BodyParser.__init__(mock_self, fields)

        # Assert
        mock_self._create_parser.assert_called_once()
        self.assertEqual(
            mock_self.fields,
            mock_self._create_parser.return_value.parse_args.return_value
        )

    def test_create_parser_returns_parser_with_all_fields(self):
        # Setup
        mock_self = MagicMock(
            fields=[
                {'name': 'username', 'type': str, 'location': 'form', 'required': True},
                {'name': 'password', 'type': str, 'location': 'form', 'required': True}
            ]
        )
        expected_calls = [
            call(
                name='username',
                type=str,
                location='form',
                required=True
            ),
            call(
                name='password',
                type=str,
                location='form',
                required=True
            )
        ]

        # Act
        BodyParser._create_parser(mock_self)

        # Assert
        self.mocks['flask_parser_mock'].return_value.\
            add_argument.assert_has_calls(expected_calls)
