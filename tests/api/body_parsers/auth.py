import unittest

from users.api.body_parsers.auth import AuthParser, BaseParser


class AuthParserTestCase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(AuthParser, BaseParser))
