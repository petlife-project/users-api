from werkzeug.datastructures import FileStorage


AUTH_FIELDS = [
    {'name': 'username', 'type': str, 'location': 'json', 'required': True},
    {'name': 'password', 'type': str, 'location': 'json', 'required': True},
    {'name': 'type', 'type': str, 'location': 'json', 'required': True,
     'choices': ['client', 'shop']}
]


SHOP_UPDATE_FIELDS = [
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


CLIENT_UPDATE_FIELDS = [
    {'name': 'name', 'type': str, 'location': 'json', 'required': False, 'store_missing': False},
    {'name': 'email', 'type': str, 'location': 'json', 'required': False, 'store_missing': False},
    {'name': 'address', 'type': str, 'location': 'json', 'required': False, 'store_missing': False},
    {'name': 'phone_number', 'type': str, 'location': 'json', 'required': False,
     'store_missing': False},
    {'name': 'pets', 'type': dict, 'location': 'json', 'required': False, 'store_missing': False}
]


SHOP_REGISTRATION_FIELDS = [
    {'name': 'username', 'type': str, 'location': 'json', 'required': True},
    {'name': 'password', 'type': str, 'location': 'json', 'required': True},
    {'name': 'name', 'type': str, 'location': 'json', 'required': True},
    {'name': 'email', 'type': str, 'location': 'json', 'required': True},
    {'name': 'address', 'type': str, 'location': 'json', 'required': True},
    {'name': 'phone_number', 'type': str, 'location': 'json', 'required': True},
    {'name': 'cnpj', 'type': str, 'location': 'json', 'required': True}
]


CLIENT_REGISTRATION_FIELDS = [
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
    {'name': 'service_id', 'type': str, 'location': 'args', 'required': True}
]


PET_REMOVAL = [
    {'name': 'pet_name', 'type': str, 'location': 'args', 'required': True}
]
