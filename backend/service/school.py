from req import Service
from service.base import BaseService
from utils.form import form_validation

class SchoolService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        SchoolService.inst = self

    def get_school_list(self):
        res = yield self.db.execute('SELECT * FROM schools;')
        return (None, res.fetchall())

    def get_school(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('SELECT * FROM schools WHERE id=%s;', (data['id'],))
        if res.rowcount == 0:
            return ('No school ID', None)
        return (None, res.fetchone())
