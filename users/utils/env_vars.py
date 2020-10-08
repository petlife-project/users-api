import os


# MongoDB
MONGO_CONNECTION_STRING = str(os.environ.get('MONGO_CONNECTION_STRING'))
CLIENTS_COLLECTION = str(os.environ.get('MONGO_CLIENTS_COLLECTION'))
SHOPS_COLLECTION = str(os.environ.get('MONGO_SHOPS_COLLECTION'))

# COS
COS_API_KEY = str(os.environ.get('COS_API_KEY'))
COS_RESOURCE_INSTANCE_ID = str(os.environ.get('COS_RESOURCE_INSTANCE_ID'))
COS_ENDPOINT = str(os.environ.get('COS_ENDPOINT'))
