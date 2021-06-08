# pylint: disable = import-error
import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from cheroot.wsgi import PathInfoDispatcher
from cheroot.wsgi import Server as WSGIServer

from users.api.routes.client import Client
from users.api.routes.shop import Shop
from users.api.routes.auth import Auth

from users.utils.env_vars import JWT_PRIVATE_PEM, JWT_TOKEN_TTL,\
    JWT_ALGORITHM, JWT_PUBLIC_PEM

APP = Flask(__name__)
APP.config['JWT_ALGORITHM'] = JWT_ALGORITHM
APP.config['JWT_PRIVATE_KEY'] = JWT_PRIVATE_PEM
APP.config['JWT_PUBLIC_KEY'] = JWT_PUBLIC_PEM
APP.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=JWT_TOKEN_TTL)
JWTManager(APP)

CORS(APP)
API = Api(APP)
PORT = int(os.getenv('PORT', '8080'))

DISPATCHER = PathInfoDispatcher({'/': APP})
SERVER = WSGIServer(('0.0.0.0', PORT), DISPATCHER)

API.add_resource(Client, '/client')
API.add_resource(Shop, '/shop')
API.add_resource(Auth, '/auth')

if __name__ == '__main__':
    print(f'Server running on port {PORT}')
    SERVER.safe_start()
