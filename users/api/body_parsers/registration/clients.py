from users.api.body_parsers.registration.base import BaseRegParser


class ClientRegParser(BaseRegParser):
    """ Parser for POST requests on the clients route
    """

    def __init__(self):
        self._additional_fields.extend([
            {'name': 'cpf', 'type': str, 'location': 'form', 'required': False}
        ])
        super().__init__()
