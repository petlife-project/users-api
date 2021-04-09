from flask_restful import abort

from users.utils.db.adapter_factory import get_mongo_adapter
from users.utils.env_vars import SHOPS_COLLECTION


# pylint: disable=inconsistent-return-statements
class GetAllService:
    """ Service responsible for getting a list of
        all the shops registered in the system.
    """
    def get(self):
        shops_list = self._get_from_mongo()
        return shops_list

    @staticmethod
    def _get_from_mongo():
        mongo = get_mongo_adapter()
        try:
            return mongo.get_users(SHOPS_COLLECTION)

        except KeyError as error:
            abort(404, extra=f'{error}')
