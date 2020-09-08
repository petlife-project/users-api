import unittest
from unittest.mock import patch, MagicMock

from users.utils.db.storage_adapter import StorageAdapter, ClientError


class StorageAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        ibm_boto3_patch = patch('users.utils.db.storage_adapter.ibm_boto3')
        self.mocks['ibm_boto3_mock'] = ibm_boto3_patch.start()
        self.patches.append(ibm_boto3_patch)

        config_patch = patch('users.utils.db.storage_adapter.Config')
        self.mocks['config_mock'] = config_patch.start()
        self.patches.append(config_patch)

        api_key_patch = patch('users.utils.db.storage_adapter.COS_API_KEY',
                        new='mock_api_key')
        self.mocks['api_key_mock'] = api_key_patch.start()
        self.patches.append(api_key_patch)

        endpoint_patch = patch('users.utils.db.storage_adapter.COS_ENDPOINT',
                        new='mock_endpoint')
        self.mocks['endpoint_mock'] = endpoint_patch.start()
        self.patches.append(endpoint_patch)

        resource_id_patch = patch('users.utils.db.storage_adapter.COS_RESOURCE_INSTANCE_ID',
                        new='mock_resource_id')
        self.mocks['resource_id_mock'] = resource_id_patch.start()
        self.patches.append(resource_id_patch)

        os_patch = patch('users.utils.db.storage_adapter.os')
        self.mocks['os_mock'] = os_patch.start()
        self.patches.append(os_patch)

        gen_id_patch = patch('users.utils.db.storage_adapter.generate_id')
        self.mocks['gen_id_mock'] = gen_id_patch.start()
        self.patches.append(gen_id_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_s3_resource(self):
        # Setup
        mock_self = MagicMock()

        # Act
        StorageAdapter.__init__(mock_self)

        # Assert
        self.mocks['ibm_boto3_mock'].client.assert_called_with(
            's3',
            ibm_api_key_id='mock_api_key',
            ibm_service_instance_id='mock_resource_id',
            config=self.mocks['config_mock'].return_value,
            endpoint_url='mock_endpoint'
        )

    def test_upload_successful_run_id_provided(self):
        # Setup
        mock_self = MagicMock(bucket='test_bucket')
        file_mock = MagicMock(filename='test.png')
        file_id = 'random_string.png'

        # Act
        new_upload = StorageAdapter.upload(mock_self, file_mock, file_id)

        # Assert
        self.mocks['gen_id_mock'].assert_not_called()
        self.mocks['os_mock'].path.splitext.assert_not_called()
        mock_self.client.upload_fileobj.assert_called_with(
            Fileobj=file_mock,
            Bucket='test_bucket',
            Key='random_string.png',
            Config=self.mocks['ibm_boto3_mock'].s3.transfer.TransferConfig.return_value
        )
        file_mock.close.assert_called()
        self.assertEqual(new_upload, 'random_string.png')

    def test_upload_successful_run_id_generated(self):
        # Setup
        mock_self = MagicMock(bucket='test_bucket')
        file_mock = MagicMock(filename='test.png')
        self.mocks['gen_id_mock'].return_value = 'random_string'
        self.mocks['os_mock'].path.splitext.return_value = ('test', '.png')

        # Act
        new_upload = StorageAdapter.upload(mock_self, file_mock)

        # Assert
        self.mocks['gen_id_mock'].assert_called()
        self.mocks['os_mock'].path.splitext.assert_called_with('test.png')
        mock_self.client.upload_fileobj.assert_called_with(
            Fileobj=file_mock,
            Bucket='test_bucket',
            Key='random_string.png',
            Config=self.mocks['ibm_boto3_mock'].s3.transfer.TransferConfig.return_value
        )
        file_mock.close.assert_called()
        self.assertEqual(new_upload, 'random_string.png')

    def test_upload_except_client_error(self):
        # Setup
        mock_self = MagicMock()
        file_mock = MagicMock()
        self.mocks['gen_id_mock'].return_value = 'random_string'
        self.mocks['os_mock'].path.splitext.return_value = ('test', '.png')
        mock_self.client.upload_fileobj.side_effect = ClientError

        # Act & Assert
        with self.assertRaises(RuntimeError):
            StorageAdapter.upload(mock_self, file_mock)

    def test_upload_except_exception(self):
        # Setup
        mock_self = MagicMock()
        file_mock = MagicMock()
        mock_self.client.upload_fileobj.side_effect = Exception

        # Act & Assert
        with self.assertRaises(RuntimeError):
            StorageAdapter.upload(mock_self, file_mock)

    def test_download_successful_run(self):
        # Setup
        mock_self = MagicMock(bucket='test_bucket')
        file_id = 'test_random'
        mock_self.client.get_object.return_value = {'Body': 'here be bytes'}

        # Act
        download = StorageAdapter.download(mock_self, file_id)

        # Assert
        mock_self.client.get_object.assert_called_with(
            Bucket='test_bucket',
            Key='test_random'
        )
        self.assertEqual(download, 'here be bytes')

    def test_download_except_client_error(self):
        # Setup
        mock_self = MagicMock(bucket='test_bucket')
        file_id = 'random_string'
        mock_self.client.get_object.side_effect = ClientError

        # Act & Assert
        with self.assertRaises(RuntimeError):
            StorageAdapter.download(mock_self, file_id)

    def test_download_except_exception(self):
        # Setup
        mock_self = MagicMock(bucket='test_bucket')
        file_id = 'random_string'
        mock_self.client.get_object.side_effect = Exception

        # Act & Assert
        with self.assertRaises(RuntimeError):
            StorageAdapter.download(mock_self, file_id)

    def test_delete_successful_run(self):
        # Setup
        mock_self = MagicMock(
            bucket='test_bucket',
            client=MagicMock(
                exceptions=MagicMock(
                    NoSuchKey=Exception
                )
            )
        )
        file_id = 'some_file'
        mock_self.client.get_object.side_effect = \
            mock_self.client.exceptions.NoSuchKey

        # Act
        deleted = StorageAdapter.delete(mock_self, file_id)

        # Assert
        mock_self.client.delete_object.assert_called_with(
            Bucket='test_bucket',
            Key='some_file'
        )
        self.assertEqual(deleted, True)

    def test_delete_except_client_error(self):
        # Setup
        mock_self = MagicMock()
        file_id = 'some_file'
        mock_self.client.delete_object.side_effect = ClientError

        # Act & Assert
        with self.assertRaises(RuntimeError):
            StorageAdapter.delete(mock_self, file_id)

    def test_delete_except_exception(self):
        # Setup
        mock_self = MagicMock()
        file_id = 'some_file'
        mock_self.client.delete_object.side_effect = Exception

        # Act & Assert
        with self.assertRaises(RuntimeError):
            StorageAdapter.delete(mock_self, file_id)

    def test_replace_successful_run(self):
        # Setup
        mock_self = MagicMock()
        file_mock = MagicMock()
        file_id = 'some_id'
        mock_self.delete.return_value = True
        mock_self.upload.return_value = 'replaced_file'

        # Act
        new_file = StorageAdapter.replace(mock_self, file_id, file_mock)

        # Assert
        mock_self.delete.assert_called_with('some_id')
        self.assertEqual(new_file, 'replaced_file')

    def test_replace_operation_raises_runtime_error(self):
        # Setup
        mock_self = MagicMock()
        file_mock = MagicMock()
        file_id = 'some_id'
        mock_self.delete.return_value = False

        # Act & Assert
        with self.assertRaises(RuntimeError):
            StorageAdapter.replace(mock_self, file_id, file_mock)
