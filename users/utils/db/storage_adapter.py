import os

import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError

from users.utils.env_vars import COS_API_KEY, COS_ENDPOINT, \
    COS_RESOURCE_INSTANCE_ID
from users.utils.id_generator import generate_id


# pylint: disable=no-member
class StorageAdapter:
    """ Wrapper for connecting and doing operations with IBM COS
    """

    def __init__(self):
        self.client = ibm_boto3.client(
            's3',
            ibm_api_key_id=COS_API_KEY,
            ibm_service_instance_id=COS_RESOURCE_INSTANCE_ID,
            config=Config(signature_version='oauth'),
            endpoint_url=COS_ENDPOINT
        )
        self.bucket = 'petlife-shops-pics'

    def upload(self, file_obj, existing_file_id=None):
        """ Uploads a file to the bucket with a generated name

            The S3.Object.upload_fileobj method automatically runs
            a multi-part upload when necessary. In this case, 5MB parts
            when the file is over 15MB.

            Args:
                file_obj (werkzeug.datastructures.FileStorage):
                    An object representing a file from the request

            Raises:
                RuntimeError: If any errors occur during operation

            Returns:
                file_id (str): The name of the uploaded file
        """
        file_id = existing_file_id if existing_file_id \
            else f'{generate_id()}{os.path.splitext(file_obj.filename)[1]}'
        file_obj.filename = file_id

        try:
            part_size = 1024 * 1024 * 5
            file_threshold = 1024 * 1024 * 15

            transfer_config = ibm_boto3.s3.transfer.TransferConfig(
                multipart_threshold=file_threshold,
                multipart_chunksize=part_size
            )

            self.client.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.bucket,
                Key=file_id,
                Config=transfer_config
            )
            file_obj.close()

            return file_id

        except ClientError as error:
            error_message = f'Error when uploading file to COS: {error}'
            print(error_message)
            raise RuntimeError(error_message) from error

        except Exception as error:
            error_message = f'Unexpected error occurred when uploading to COS: {error}'
            print(error_message)
            raise RuntimeError(error_message) from error

    def download(self, file_id):
        """ Downloads a file from the bucket with the specified name

            Args:
                file_id (str): The name of the file in the bucket

            Raises:
                RuntimeError: If any errors occur during operation

            Returns:
                file (obj): File object representing a binary
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket,
                Key=file_id
            )
            return response['Body']

        except ClientError as error:
            error_message = f'Error when downloading file from COS: {error}'
            print(error_message)
            raise RuntimeError(error_message) from error

        except Exception as error:
            error_message = f'Unexpected error occurred when downloading from COS: {error}'
            print(error_message)
            raise RuntimeError(error_message) from error

    def delete(self, file_id):
        """ Finds and deletes a file from the bucket

            As ibm-cos delete method doesn't return whether
            the deletion was successful or not, this method
            checks for the file right after deleting it to
            assert the operation worked as expected.

            Args:
                file_id (str): The name of the file in the bucket

            Raises:
                RuntimeError: If any errors occur during operation

            Returns:
                bool: Deleted or not
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket,
                Key=file_id
            )
            try:
                self.client.get_object(
                    Bucket=self.bucket,
                    Key=file_id
                )
                return False
            except self.client.exceptions.NoSuchKey:
                return True

        except ClientError as error:
            error_message = f'Error when deleting file from COS: {error}'
            print(error_message)
            raise RuntimeError(error_message) from error

        except Exception as error:
            error_message = f'Unexpected error occurred when deleting from COS: {error}'
            print(error_message)
            raise RuntimeError(error_message) from error

    def replace(self, file_id, new_file):
        """ Finds and replaces a file from the bucket

            Args:
                file_id (str): The file's name in the bucket
                new_file (werkzeug.datastructures.FileStorage):
                    An object representing a file from the request

            Raises:
                RuntimeError: If anything goes wrong with either one of the operations

            Returns:
                new_ (str): New file's id. Same id, but extension may differ from previous
        """
        if self.delete(file_id):
            return self.upload(new_file, file_id)
        raise RuntimeError(f'Not able to delete {file_id}')
 