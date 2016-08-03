from req import Service
from service.base import BaseService


class Bulletin(BaseService):
    def get_bulletin_list(self, data):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM bulletins WHERE group_id=%s", (data['group_id'],))
        res = res.fetchall()
        if res is None:
            res = []
        return (None, res)
