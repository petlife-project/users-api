from users.api.body_parsers.base import BaseParser


class AuthParser(BaseParser):
    """ Parser for requests on the authentication route
    """

    def __init__(self):
        self._additional_fields.extend([
            {'name': 'type', 'type': str, 'location': 'form', 'required': True,
             'choices': ['client', 'shop']}
        ])
        super().__init__()
