from req import Service
from service.base import BaseService


class Language(BaseService):
    def get_language_list(self):
        res = yield self.db.execute("SELECT * FROM languages")
        res = res.fetchall()
        if res is None:
            res = []
        return (None, res)
