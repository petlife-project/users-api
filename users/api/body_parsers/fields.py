from werkzeug.datastructures import FileStorage


AUTH_FIELDS = [
    {'name': 'username', 'type': str, 'location': 'json', 'required': True},
    {'name': 'password', 'type': str, 'location': 'json', 'required': True},
    {'name': 'type', 'type': str, 'location': 'json', 'required': True,
     'choices': ['client', 'shop']}
]


SHOPS_UPDATE_FIELDS = [
    {'name': 'username', 'type': str, 'location': 'json', 'required': True},
    {'name': 'password', 'type': str, 'location': 'json', 'required': True},
    {'name': 'email', 'type': str, 'location': 'json', 'required': False,
     'store_missing': False},
    {'name': 'address', 'type': str, 'location': 'json', 'required': False,
     'store_missing': False},
    {'name': 'phone_number', 'type': str, 'location': 'json', 'required': False,
     'store_missing': False},
    {'name': 'services', 'type': dict, 'location': 'json', 'required': False,
     'store_missing': False},
    {'name': 'description', 'type': str, 'location': 'json', 'required': False,
     'store_missing': False},
    {'name': 'hours', 'type': str, 'location': 'json', 'required': False,
     'store_missing': False},
    {'name': 'profile_pic', 'type': FileStorage, 'location': 'files', 'required': False,
     'store_missing': False},
    {'name': 'banner_pic', 'type': FileStorage, 'location': 'files', 'required': False,
     'store_missing': False}
]


CLIENTS_UPDATE_FIELDS = [
    {'name': 'username', 'type': str, 'location': 'json', 'required': True},
    {'name': 'password', 'type': str, 'location': 'json', 'required': True},
    {'name': 'name', 'type': str, 'location': 'json', 'required': False,
        'store_missing': False},
    {'name': 'email', 'type': str, 'location': 'json', 'required': False,
        'store_missing': False},
    {'name': 'address', 'type': str, 'location': 'json', 'required': False,
        'store_missing': False},
    {'name': 'phone_number', 'type': str, 'location': 'json', 'required': False,
        'store_missing': False},
    {'name': 'pets', 'type': dict, 'location': 'json', 'required': False,
        'store_missing': False}
]


SHOPS_REGISTRATION_FIELDS = [
    {'name': 'username', 'type': str, 'location': 'json', 'required': True},
    {'name': 'password', 'type': str, 'location': 'json', 'required': True},
    {'name': 'name', 'type': str, 'location': 'json', 'required': True},
    {'name': 'email', 'type': str, 'location': 'json', 'required': True},
    {'name': 'address', 'type': str, 'location': 'json', 'required': True},
    {'name': 'phone_number', 'type': str, 'location': 'json', 'required': True},
    {'name': 'cnpj', 'type': str, 'location': 'json', 'required': True}
]


CLIENTS_REGISTRATION_FIELDS = [
    {'name': 'username', 'type': str, 'location': 'json', 'required': True},
    {'name': 'password', 'type': str, 'location': 'json', 'required': True},
    {'name': 'name', 'type': str, 'location': 'json', 'required': True},
    {'name': 'email', 'type': str, 'location': 'json', 'required': True},
    {'name': 'address', 'type': str, 'location': 'json', 'required': True},
    {'name': 'phone_number', 'type': str, 'location': 'json', 'required': True},
    {'name': 'cpf', 'type': str, 'location': 'json', 'required': False,
     'store_missing': False}
]

SERVICE_REMOVAL = [
    {'name': 'username', 'type': str, 'location': 'args', 'required': True},
    {'name': 'password', 'type': str, 'location': 'args', 'required': True},
    {'name': 'service_id', 'type': str, 'location': 'args', 'required': True},
]
