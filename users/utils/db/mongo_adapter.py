from bson.objectid import ObjectId

from pymongo import MongoClient
from pymongo.collection import ReturnDocument
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
                doc with id
        """
        username = doc.get('username')
        try:
            self.db_[collection].insert_one(doc)
            doc['_id'] = str(doc['_id'])
            del doc['password']
            # PyMongo's insert_one modifies the input value
            # instead of returning a modified version (yikes)
            # so there's no need to return the value, as the "doc"
            # variable where this method is called is already altered.

        except DuplicateKeyError as error:
            raise KeyError(f'User {username} already exists in {collection}') from error

    def update(self, collection, doc, user_id):
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
        filter_ = self._get_id_filter(user_id)
        try:
            updated = None
            if doc.get('services'):
                updated = self.db_[collection].find_one_and_update(
                    filter_,
                    {'$push': {'services': doc.get('services')}},
                    projection={'password': False},
                    return_document=ReturnDocument.AFTER
                )
                del doc['services']

            if doc.get('pets'):
                updated = self.db_[collection].find_one_and_update(
                    filter_,
                    {'$push': {'pets': doc.get('pets')}},
                    projection={'password': False},
                    return_document=ReturnDocument.AFTER
                )
                del doc['pets']

            if doc:
                updated = self.db_[collection].find_one_and_update(
                    filter_,
                    {'$set': doc},
                    projection={'password': False},
                    return_document=ReturnDocument.AFTER
                )

            if not updated:
                raise KeyError('Invalid user id')

            updated['_id'] = str(updated['_id'])
            return updated

        except PyMongoError as error:
            print(f'Error when performing update on MongoDB: {error}')
            raise RuntimeError from error

    def remove(self, collection, doc, user_id):
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
        filter_ = self._get_id_filter(user_id)
        try:
            if doc.get('service_id'):
                alteration = {'$pull': {'services': {'service_id': doc['service_id']}}}
            elif doc.get('pet_name'):
                alteration = {'$pull': {'pets': {'name': doc['pet_name']}}}

            updated = self.db_[collection].find_one_and_update(
                filter_,
                alteration,
                projection={'password': False},
                return_document=ReturnDocument.AFTER
            )

            if not updated:
                raise KeyError('No object found with set name/id')

            updated['_id'] = str(updated['_id'])
            return updated

        except PyMongoError as error:
            print(f'Error when performing update on MongoDB: {error}')
            raise RuntimeError from error

    def delete(self, collection, user_id):
        """ Finds and deletes a document in a collection

            Args:
                collection (str): The collection where the document is
                doc (dict): The document to be deleted (must contain username field)

            Raises:
                RuntimeError: If any errors occur while doing the operation

            Returns:
                Operation's acknowledgement (bool)
        """
        filter_ = self._get_id_filter(user_id)
        try:
            self.db_[collection].delete_one(filter_)
            return True

        except PyMongoError as error:
            print(f'Error when performing deletion on MongoDB: {error}')
            raise RuntimeError from error

    def get_user_by_username(self, collection, username, password):
        """ Search for an specific user by username and password

            Args:
                collection (str): The collection to be searched on
                username (str): The username to search
                password (str): Must be exact match

            Returns:
                user_obejct (dict): The whole user object stored in MongoDB
        """
        query = {'username': username, 'password': password}
        user = self.db_[collection].find_one(query, projection={'password': False})

        if not user:
            raise KeyError('Invalid username or password')

        user['_id'] = str(user['_id'])
        return user

    def get_users(self, collection):
        """ Search for all the users in a collection

            Args:
                collection (str): The collection to be searched on

            Returns:
                result_list (list): List of found documents
        """
        result_list = list(self.db_[collection].find({}, projection={'password': False}))

        if not result_list:
            raise KeyError('No users yet')

        for user in result_list:
            user['_id'] = str(user['_id'])

        return result_list

    @staticmethod
    def _get_id_filter(user_id):
        return {'_id': ObjectId(user_id)}
