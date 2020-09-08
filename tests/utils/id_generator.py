import unittest

from users.utils.id_generator import generate_id


class GeneratorIdTestcase(unittest.TestCase):
    def test_generate_id_return_standard_length(self):
        # Act
        key = generate_id()

        # Assert
        self.assertIsInstance(key, str)
