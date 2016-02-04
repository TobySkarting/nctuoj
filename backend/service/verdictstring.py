from req import Service
from service.base import BaseService

class VerdictStringService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        VerdictStringService.inst = self

    def get_verdict_string_map(self):
        # res = self.rs.get('verdict_string')
        # if res: return res
        res  = yield self.db.execute('SELECT * FROM map_verdict_string;')
        res = res.fetchall()
        map_verdict_string = {x['id']: dict(x) for x in res}
        map_string_verdict = {x['abbreviation']: dict(x) for x in res}
        # self.rs.set('verdict_string', (map_verdict_string, map_string_verdict))
        return (map_verdict_string, map_string_verdict)

