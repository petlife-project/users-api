import unittest
from unittest.mock import patch, MagicMock, call

from users.utils.db.mongo_adapter import MongoAdapter, DuplicateKeyError, PyMongoError


# pylint: disable=protected-access
class MongoAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        obj_id_patch = patch('users.utils.db.mongo_adapter.ObjectId')
        self.mocks['obj_id'] = obj_id_patch.start()
        self.patches.append(obj_id_patch)

        mongo_patch = patch('users.utils.db.mongo_adapter.MongoClient')
        self.mocks['mongo'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        conn_str = patch('users.utils.db.mongo_adapter.MONGO_CONNECTION_STRING',
                         new='mock_connection')
        self.mocks['conn_str'] = conn_str.start()
        self.patches.append(conn_str)

        return_doc_patch = patch('users.utils.db.mongo_adapter.ReturnDocument')
        self.mocks['return_doc'] = return_doc_patch.start()
        self.patches.append(return_doc_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_client_created(self):
        # Setup
        mock_self = MagicMock()

        # Act
        MongoAdapter.__init__(mock_self)

        # Assert
        self.mocks['mongo'].assert_called_with(
            'mock_connection',
            connect=True
        )

    def test_create_successful_run(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test'
        doc = {
            'username': 'unique_user',
            'name': 'chad'
        }
        mock_self.db_['test'].insert_one.side_effect = doc.update(
            _id='mongo_created_id',
            password='password_test'
        )

        # Act
        MongoAdapter.create(mock_self, collection, doc)

        # Assert
        mock_self.db_['test'].insert_one.assert_called_with(
            {'username': 'unique_user', 'name': 'chad', '_id': 'mongo_created_id'}
        )
        self.assertEqual(doc, {
            'username': 'unique_user',
            'name': 'chad',
            '_id': 'mongo_created_id'
        })

    def test_create_doc_already_exists(self):
        # Setup
        mock_self = MagicMock()
        mock_self.db_['test'].insert_one.side_effect = DuplicateKeyError(MagicMock)
        collection = 'test'
        doc = {
            'username': 'unique_user',
            'name': 'chad'
        }

        # Act & Assert
        with self.assertRaises(KeyError):
            MongoAdapter.create(mock_self, collection, doc)

    def test_update_not_updating_list_fields_updated_document(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test'
        doc = {'test_field': 'new_value'}
        user_id = 'polar_bear'

        # Act
        MongoAdapter.update(mock_self, collection, doc, user_id)

        # Assert
        mock_self.db_['test'].find_one_and_update.assert_called_with(
            mock_self._get_id_filter.return_value,
            {'$set': {'test_field': 'new_value'}},
            projection={'password': False},
            return_document=self.mocks['return_doc'].AFTER
        )

    def test_update_updating_list_field_updated_document(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test'
        doc = {'services': 'new_service', 'pets': 'new_pet'}
        user_id = 'polar_bear'
        find_calls = [
            call(
                mock_self._get_id_filter.return_value,
                {'$push': {'services': 'new_service'}},
                projection={'password': False},
                return_document=self.mocks['return_doc'].AFTER
            ),
            call(
                mock_self._get_id_filter.return_value,
                {'$push': {'pets': 'new_pet'}},
                projection={'password': False},
                return_document=self.mocks['return_doc'].AFTER
            )
        ]

        # Act
        MongoAdapter.update(mock_self, collection, doc, user_id)

        # Assert
        mock_self.db_['test'].find_one_and_update.assert_has_calls(find_calls)

    def test_update_document_not_found_no_update_raises_key_error(self):
        # Arrange
        mock_self = MagicMock()
        collection = 'test'
        doc = {}
        user_id = 'polar_bear'

        # Act & Assert
        with self.assertRaises(KeyError):
            MongoAdapter.update(mock_self, collection, doc, user_id)

    def test_update_document_unexpected_error_raises_runtime_error(self):
        # Arrange
        mock_self = MagicMock()
        collection = 'test'
        doc = {'something': 'testing'}
        mock_self.db_['test'].find_one_and_update.side_effect = PyMongoError()
        user_id = 'polar_bear'

        # Act & Assert
        with self.assertRaises(RuntimeError):
            MongoAdapter.update(mock_self, collection, doc, user_id)

    def test_remove_removes_service_updated_document(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test'
        doc = {'service_id': 'some_id'}
        user_id = 'polar_bear'

        # Act
        MongoAdapter.remove(mock_self, collection, doc, user_id)

        # Assert
        mock_self.db_['test'].find_one_and_update.assert_called_with(
            mock_self._get_id_filter.return_value,
            {'$pull': {'services': {'service_id': 'some_id'}}},
            projection={'password': False},
            return_document=self.mocks['return_doc'].AFTER
        )

    def test_remove_removes_pet_updated_document(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test'
        doc = {'pet_name': 'some_name'}
        user_id = 'polar_bear'

        # Act
        MongoAdapter.remove(mock_self, collection, doc, user_id)

        # Assert
        mock_self.db_['test'].find_one_and_update.assert_called_with(
            mock_self._get_id_filter.return_value,
            {'$pull': {'pets': {'name': 'some_name'}}},
            projection={'password': False},
            return_document=self.mocks['return_doc'].AFTER
        )

    def test_remove_not_found_no_update_raises_key_error(self):
        # Arrange
        mock_self = MagicMock()
        collection = 'test'
        doc = {'service_id': 'test_id'}
        user_id = 'polar_bear'
        mock_self.db_['test'].find_one_and_update.return_value = None

        # Act & Assert
        with self.assertRaises(KeyError):
            MongoAdapter.remove(mock_self, collection, doc, user_id)

    def test_remove_unexpected_error_raises_runtime_error(self):
        # Arrange
        mock_self = MagicMock()
        collection = 'test'
        doc = {'service_id': 'test_id'}
        user_id = 'polar_bear'
        mock_self.db_['test'].find_one_and_update.side_effect = PyMongoError()

        # Act & Assert
        with self.assertRaises(RuntimeError):
            MongoAdapter.remove(mock_self, collection, doc, user_id)

    @staticmethod
    def test_delete_successful_run_deleted_document():
        # Setup
        mock_self = MagicMock()
        collection = 'test'
        user_id = 'polar_bear'

        # Act
        MongoAdapter.delete(mock_self, collection, user_id)

        # Assert
        mock_self.db_['test'].delete_one.assert_called_with(
            mock_self._get_id_filter.return_value
        )

    def test_delete_except_pymongoerror(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test'
        user_id = 'polar_bear'
        mock_self.db_['test'].delete_one.side_effect = PyMongoError

        # Act & Assert
        with self.assertRaises(RuntimeError):
            MongoAdapter.delete(mock_self, collection, user_id)

    def test_get_user_by_username_found_user_returns_it(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test_col'
        username = 'user'
        password = 'password'
        mock_self.db_['test_col'].find_one.return_value = {
            '_id': 1234,
            'other': 'fields'
        }

        # Act
        user = MongoAdapter.get_user_by_username(mock_self, collection, username, password)

        # Assert
        self.assertEqual(user, {'_id': '1234', 'other': 'fields'})

    def test_get_user_by_username_not_found_raises_keyerror(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test_col'
        username = 'user'
        password = 'password'
        mock_self.db_['test_col'].find_one.return_value = None

        # Act & Assert
        with self.assertRaises(KeyError):
            MongoAdapter.get_user_by_username(mock_self, collection, username, password)

    def test_get_users_returns_list(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test_col'
        mock_self.db_['test_col'].find.return_value = [
            {'_id': 123},
            {'_id': 456},
            {'_id': 789}
        ]

        # Act
        list_ = MongoAdapter.get_users(mock_self, collection)

        # Assert
        self.assertEqual(list_, [
            {'_id': '123'},
            {'_id': '456'},
            {'_id': '789'}
        ])

    def test_get_users_nothing_found_raises_keyerror(self):
        # Setup
        mock_self = MagicMock()
        collection = 'test_col'
        mock_self.db_['test_col'].find.return_value = []

        # Act & Assert
        with self.assertRaises(KeyError):
            MongoAdapter.get_users(mock_self, collection)

    def test_get_id_filter_returns_obj_id_in_dict(self):
        # Setup
        user_id = 'user_id'

        # Act
        id_filter = MongoAdapter._get_id_filter(user_id)

        # Assert
        self.assertEqual(id_filter, {'_id': self.mocks['obj_id']()})
