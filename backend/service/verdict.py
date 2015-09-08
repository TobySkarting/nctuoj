from service.base import BaseService
import config

class VerdictService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        VerdictService.inst = self

    def get_verdict_list(self, data={}):
        res = self.rs.get('verdict_list')
        if res: return (None, res)
        sql = "SELECT v.*, u.account as setter_user FROM verdicts as v, users as u WHERE v.setter_user_id=u.id"
        res, res_cnt = yield from self.db.execute(sql)
        self.rs.set('verdict_list', res)
        return (None, res)

    
    def get_verdict(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('verdict@%s'%str(data['id']))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT v.*, u.account as setter_user FROM verdicts as v, users as u WHERE v.id=%s AND v.setter_user_id=u.id;', (data['id'],))
        if res_cnt == 0:
            return ('No Verdict ID', None)
        re = res[0]
        self.rs.set('verdict@%s'%(str(data['id'])), res)
        return (None, res)

    def delete_verdict(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        yield from self.db.execute('DELETE FROM verdicts WHERE id=%s;', (data['id'],))
        self.rs.delete('verdict_list')
        self.rs.delete('verdict@%s'%(str(data['id'])))
        return (None, str(data['id']))


