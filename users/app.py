import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from cheroot.wsgi import PathInfoDispatcher
from cheroot.wsgi import Server as WSGIServer

from users.api.routes.clients import Clients
from users.api.routes.shops import Shops
from users.api.routes.auth import Auth

APP = Flask(__name__)
CORS(APP)
API = Api(APP)
PORT = int(os.getenv('PORT', '8080'))

DISPATCHER = PathInfoDispatcher({'/': APP})
SERVER = WSGIServer(('0.0.0.0', PORT), DISPATCHER)

API.add_resource(Clients, '/clients')
API.add_resource(Shops, '/shops')
API.add_resource(Auth, '/auth')

if __name__ == '__main__':
    print(f'Server running on port {PORT}')
    SERVER.safe_start()
