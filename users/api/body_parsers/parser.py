from flask_restful.reqparse import RequestParser


class BodyParser:
    """ Class for parsing the fields provided in the list
    """

    def __init__(self, fields):
        self.fields = fields
        parser = self._create_parser()
        self.fields = parser.parse_args()

    def _create_parser(self):
        parser = RequestParser()
        for item in self.fields:
            parser.add_argument(**item)

        return parser
