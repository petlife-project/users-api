from flask_restful.reqparse import RequestParser


class BaseParser:
    """ Base request parser which others will inherit from
    """

    _base_fields = [
        {'name': 'username', 'type': str, 'location': 'form', 'required': True},
        {'name': 'password', 'type': str, 'location': 'form', 'required': True}
    ]

    _additional_fields = []

    def __init__(self):
        parser = self._create_parser()
        self.fields = parser.parse_args()

    def _create_parser(self):
        """ Create a request parser with all the field
        """

        parser = RequestParser()
        for item in self._base_fields:
            parser.add_argument(**item)

        for item in self._additional_fields:
            parser.remove_argument(item['name'])
            parser.add_argument(**item)

        return parser
