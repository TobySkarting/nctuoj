from service.base import BaseService
import config

class VerdictService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        VerdictService.inst = self

    def get_verdict_list(self, data={}):
        res = self.rs.get('verdict_list')
        if res: return (None, res)
        sql = "SELECT v.*, u.account as setter_user FROM verdicts as e, users as u WHERE e.setter_user_id=u.id order by e.priority"
        res, res_cnt = yield from self.db.execute(sql)
        self.rs.set('verdict_list', res)
        return (None, res)

    
    def get_verdict(self, data={}):
        pass
