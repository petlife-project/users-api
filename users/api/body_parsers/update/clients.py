from users.api.body_parsers.update.base import BaseUpdateParser


class ClientUpdateParser(BaseUpdateParser):
    """ Parser for update requests on clients route
    """

    def __init__(self):
        self._additional_fields.extend([
            {'name': 'pets', 'type': str, 'location': 'form', 'required': False}
        ])
        super().__init__()
