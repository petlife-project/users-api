from users.api.body_parsers.parser import BodyParser
from users.api.body_parsers.fields import AUTH_FIELDS, \
    CLIENT_REGISTRATION_FIELDS, CLIENT_UPDATE_FIELDS, PET_REMOVAL, \
    SHOP_REGISTRATION_FIELDS, SHOP_UPDATE_FIELDS, \
    SERVICE_REMOVAL


class BodyParserFactory:
    """ Factory that creates a body parsers based on type of request
    """

    def __init__(self):
        self.types = {
            'auth': AUTH_FIELDS,
            'client_registration': CLIENT_REGISTRATION_FIELDS,
            'shop_registration': SHOP_REGISTRATION_FIELDS,
            'client_update': CLIENT_UPDATE_FIELDS,
            'shop_update': SHOP_UPDATE_FIELDS,
            'service_removal': SERVICE_REMOVAL,
            'pet_removal': PET_REMOVAL
        }

    def get_parser(self, type_):
        return BodyParser(self.types[type_])


FACTORY = BodyParserFactory()
