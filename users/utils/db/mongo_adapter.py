from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError

from users.utils.env_vars import MONGO_CONNECTION_STRING


class MongoAdapter:
    """ Wrapper for connecting with Mongo DB and doing operations.
    """

    def __init__(self):
        self.client = MongoClient(
            MONGO_CONNECTION_STRING,
            connect=True
        )
        self.db_ = self.client.petlife

    def create(self, collection, doc):
        """ Creates a document on set collection

            Args:
                collection (str): The collection to be appended
                doc (dict): The document being inserted

            Raises:
                KeyError: When document is duplicate

            Returns:
                Operation's acknowledgement (bool)
        """
        username = doc['username']
        try:
            operation = self.db_[collection].insert_one(doc)
            del doc['_id']
            return operation.acknowledged

        except DuplicateKeyError as error:
            raise KeyError(f'User {username} already exists in {collection}') from error

    def update(self, collection, doc):
        """ Finds and updates a document in a collection

            Args:
                collection (str): The collection where the document is
                doc (dict): The document or partial document to be updated
                            (must contain username field)

            Raises:
                RuntimeError: If any errors occur while doing the operation

            Returns:
                Operation's acknowledgement (bool)
        """
        filter_ = {'username': doc['username']}
        try:
            operation = self.db_[collection].update_one(filter_, {'$set': doc})
            return operation.acknowledged

        except PyMongoError as error:
            print(f'Error when performing update on MongoDB: {error}')
            raise RuntimeError from error

    def delete(self, collection, doc):
        """ Finds and deletes a document in a collection

            Args:
                collection (str): The collection where the document is
                doc (dict): The document to be deleted (must contain username field)

            Raises:
                RuntimeError: If any errors occur while doing the operation

            Returns:
                Operation's acknowledgement (bool)
        """
        filter_ = {'username': doc['username']}
        try:
            operation = self.db_[collection].delete_one(filter_)
            return operation.acknowledged

        except PyMongoError as error:
            print(f'Error when performing deletion on MongoDB: {error}')
            raise RuntimeError from error

    def get_user_information(self, collection, username):
        """ Search for an specific user by username

            Args:
                collection (str): The collection to be searched on
                username (str): The username to search

            Returns:
                user_obejct (dict): The whole user object stored in MongoDB
        """
        query = {'username': username}
        result_list = self._find(collection, query)
        user_object = result_list.pop()
        return user_object

    def _find(self, collection, query):
        """ Generic method for performing searches

            Args:
                collection (str): The collection to be searched on
                query (dict): The query specifying what to look for

            Returns:
                List of found documents
        """
        results = []
        search_result = self.db_[collection].find(query)

        for doc in search_result:
            del doc['_id']
            results.append(doc)

        return results
