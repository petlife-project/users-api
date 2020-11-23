import unittest
from unittest.mock import patch

from users.utils.db.adapter_factory import get_cos_adapter, get_mongo_adapter


class AdapterFactoryTestCase(unittest.TestCase):

    @staticmethod
    @patch('users.utils.db.adapter_factory.MongoAdapter')
    def test_get_mongo_adapter_first_call(mongo_mock):
        # Setup
        get_mongo_adapter.adapter = None

        # Act
        get_mongo_adapter()

        # Assert
        mongo_mock.assert_called()

    @staticmethod
    @patch('users.utils.db.adapter_factory.MongoAdapter')
    def test_get_mongo_adapter_subsequent_calls(mongo_mock):
        # Setup
        get_mongo_adapter.adapter = True

        # Act
        get_mongo_adapter()

        # Assert
        mongo_mock.assert_not_called()

    @staticmethod
    @patch('users.utils.db.adapter_factory.StorageAdapter')
    def test_get_cos_adapter_first_call(cos_mock):
        # Setup
        get_cos_adapter.adapter = None

        # Act
        get_cos_adapter()

        # Assert
        cos_mock.assert_called()

    @staticmethod
    @patch('users.utils.db.adapter_factory.StorageAdapter')
    def test_get_cos_adapter_subsequent_calls(cos_mock):
        # Setup
        get_cos_adapter.adapter = True

        # Act
        get_cos_adapter()

        # Assert
        cos_mock.assert_not_called()
