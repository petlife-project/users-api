import os

from users.utils.security import load_private_key, load_public_key


# MongoDB
MONGO_CONNECTION_STRING = str(os.environ.get('MONGO_CONNECTION_STRING'))
CLIENTS_COLLECTION = str(os.environ.get('MONGO_CLIENTS_COLLECTION'))
SHOPS_COLLECTION = str(os.environ.get('MONGO_SHOPS_COLLECTION'))

# COS
COS_API_KEY = str(os.environ.get('COS_API_KEY'))
COS_RESOURCE_INSTANCE_ID = str(os.environ.get('COS_RESOURCE_INSTANCE_ID'))
COS_ENDPOINT = str(os.environ.get('COS_ENDPOINT'))

# JWT
JWT_PRIVATE_PEM = load_private_key()
JWT_PUBLIC_PEM = load_public_key()
JWT_ALGORITHM = 'RS256'
JWT_TOKEN_TTL = int(os.environ.get('JWT_TOKEN_TTL', 30))
