from service.base import BaseService
import config

class ExecuteService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        ExecuteService.inst = self

    def get_execute_list(self, data={}):
        sql = "SELECT execute_types.*, u.account as setter_user  FROM execute_types INNER JOIN (SELECT id, account FROM users) as u ON execute_types.setter_user_id=u.id"
        res = yield from self.db.execute(sql)
        return (None, res)

    
    def get_execute(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['id']) == 0:
            col = ("id", "description", "lang")
            res = {}
            for x in col:
                res[x] = ""
            res['id'] = 0
            return (None, res)
        sql = "SELECT execute_types.*, u.account as setter_user  FROM execute_types INNER JOIN (SELECT id, account FROM users) as u ON execute_types.setter_user_id=u.id WHERE execute_types.id=%s"
        res = yield from self.db.execute(sql, (data["id"]))
        if len(res) == 0:
            return ('Error execute id', None)
        res = res[0]
        return (None, res)
