from users.api.body_parsers.base import BaseParser


class BaseUpdateParser(BaseParser):
    """ Base parser for update requests
    """

    def __init__(self):
        self._additional_fields.extend([
            {'name': 'name', 'type': str, 'location': 'form', 'required': False},
            {'name': 'email', 'type': str, 'location': 'form', 'required': False},
            {'name': 'address', 'type': str, 'location': 'form', 'required': False},
            {'name': 'phone_number', 'type': str, 'location': 'form', 'required': False}
        ])
        super().__init__()
