from users.utils.db.mongo_adapter import MongoAdapter
from users.utils.db.storage_adapter import StorageAdapter


def get_mongo_adapter():
    if not get_mongo_adapter.adapter:
        get_mongo_adapter.adapter = MongoAdapter()
    return get_mongo_adapter.adapter


def get_cos_adapter():
    if not get_cos_adapter.adapter:
        get_cos_adapter.adapter = StorageAdapter()
    return get_cos_adapter.adapter


get_mongo_adapter.adapter = None
get_cos_adapter.adapter = None
