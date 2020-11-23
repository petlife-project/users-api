from users.api.body_parsers.parser import BodyParser
from users.api.body_parsers.fields import AUTH_FIELDS, \
    CLIENTS_REGISTRATION_FIELDS, CLIENTS_UPDATE_FIELDS, \
    SHOPS_REGISTRATION_FIELDS, SHOPS_UPDATE_FIELDS, \
    SERVICE_REMOVAL


class BodyParserFactory:
    """ Factory that creates a body parsers based on type of request
    """

    def __init__(self):
        self.types = {
            'auth': AUTH_FIELDS,
            'client_registration': CLIENTS_REGISTRATION_FIELDS,
            'shop_registration': SHOPS_REGISTRATION_FIELDS,
            'client_update': CLIENTS_UPDATE_FIELDS,
            'shop_update': SHOPS_UPDATE_FIELDS,
            'service_removal': SERVICE_REMOVAL
        }

    def get_parser(self, type_):
        """ Chooses the parser type

            Args:
                type_ (str): Possible types are:
                    - auth
                    - client_registration
                    - shop_registration
                    - client_update
                    - shop_update
                    - service_removal

            Returns:
                BodyParser: Instance of body parser according to set type
        """
        return BodyParser(self.types[type_])


FACTORY = BodyParserFactory()
