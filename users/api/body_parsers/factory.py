from users.api.body_parsers.auth import AuthParser
from users.api.body_parsers.registration.clients import ClientRegParser
from users.api.body_parsers.registration.shops import ShopRegParser
from users.api.body_parsers.update.clients import ClientUpdateParser
from users.api.body_parsers.update.shops import ShopUpdateParser


class BodyParserFactory:
    """ Factory that creates a body parsers based on type of request
    """

    def __init__(self):
        self.types = {
            'auth': AuthParser,
            'client_registration': ClientRegParser,
            'shop_registration': ShopRegParser,
            'client_update': ClientUpdateParser,
            'shop_update': ShopUpdateParser
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

            Returns:
                BodyParser: Instance of body parser according to set type
        """
        return self.types[type_]()
