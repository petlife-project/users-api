from users.api.body_parsers.base import BaseParser


class BaseRegParser(BaseParser):
    """ Parser for registering new users
    """

    def __init__(self):
        self._additional_fields.extend([
            {'name': 'name', 'type': str, 'location': 'form', 'required': True},
            {'name': 'email', 'type': str, 'location': 'form', 'required': True},
            {'name': 'address', 'type': str, 'location': 'form', 'required': True},
            {'name': 'phone_number', 'type': str, 'location': 'form', 'required': True}
        ])
        super().__init__()
