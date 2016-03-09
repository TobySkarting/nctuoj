from req import Service
from service.base import BaseService

class ScoreService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        ScoreService.inst = self

    def get_score_types_list(self, data={}):
        res = yield self.db.execute('SELECT * from score_types;')
        res = res.fetchall()
        return (None, res)
