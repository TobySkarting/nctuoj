from req import Service
from service.base import BaseService

class SchoolService(BaseService):
    def __init__(self, db, rs, ftp):
        super().__init__(self, db, rs, ftp)
        SchoolService.inst = self

    def get_school_list(self):
        res = self.rs.get('school_list')
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT * FROM schools;')
        self.rs.set('school_list', res)
        return (None, res)

    def get_school(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute('SELECT * FROM schools WHERE id=%s;', (data['id'],))
        if res_cnt == 0:
            return ('No school ID', None)
        return (None, res[0])
