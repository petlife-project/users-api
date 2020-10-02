from werkzeug.datastructures import FileStorage

from users.api.body_parsers.update.base import BaseUpdateParser


class ShopUpdateParser(BaseUpdateParser):
    """ Parser for update requests on shops route
    """

    def __init__(self):
        self._additional_fields.extend([
            {'name': 'services', 'type': str, 'location': 'form', 'required': False},
            {'name': 'description', 'type': str, 'location': 'form', 'required': False},
            {'name': 'hours', 'type': str, 'location': 'form', 'required': False},
            {'name': 'profile_pic', 'type': FileStorage, 'location': 'files', 'required': False},
            {'name': 'banner_pic', 'type': FileStorage, 'location': 'files', 'required': False}
        ])
        super().__init__()
