from service.base import BaseService
import config

class ExecuteService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        ExecuteService.inst = self

    def get_execute_list(self, data={}):
        sql = "SELECT * FROM execute_types"
        res = yield from self.db.execute(sql)
        return (None, res)
