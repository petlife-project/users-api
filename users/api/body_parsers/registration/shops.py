from users.api.body_parsers.registration.base import BaseRegParser


class ShopRegParser(BaseRegParser):
    """ Parser for POST requests on the shops route
    """

    def __init__(self):
        self._additional_fields.extend([
            {'name': 'cnpj', 'type': str, 'location': 'form', 'required': True}
        ])
        super().__init__()
