from service.base import BaseService
import config
### need to add rs

class CommonService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        CommonService.inst = self

    def get_execute_type(self):
        res = (yield self.db.execute("SELECT * FROM execute_types order by id")).fetchall()
        ret = {}
        for x in res:
            ret[x['id']] = x
        return ret

    def get_verdict_type(self):
        res = (yield self.db.execute("SELECT * FROM map_verdict_string order by id")).fetchall()
        ret = {}
        for x in res:
            ret[x['id']] = x
        return ret
