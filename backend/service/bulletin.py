from req import Service
from service.base import BaseService
from utils.utils import HashPassword
from utils.utils import GenToken


class Bulletin(BaseService):
    def get_bulletin(self, data):
        require_args = [{
            'name': '+id',
            'type': int,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM bulletins WHERE id=%s", (data['id'],))
        res = res.fetchone()
        return (None, res)

    def post_bulletin(self, data):
        require_args = [{
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': str,
        }, {
            'name': '+title',
            'type': str,
        }, {
            'name': '+content',
            'type': str,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('bulletins', data)
        res = yield self.db.execute(sql, param)
        res = res.fetchone()
        return (None, res)

    def put_bulletin(self, data):
        require_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }, {
            'name': '+title',
            'type': str,
        }, {
            'name': '+content',
            'type': str,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        id = data.pop('id')
        sql, param = self.gen_update_sql('bulletins', data)
        yield self.db.execute(sql + " WHERE id=%s", param + (id,))
        return (None, None)

    def delete_bulletin(self, data):
        require_args = [{
            'name': '+id',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        yield self.db.execute("DELETE FROM bulletins WHERE id=%s", (data['id'],))
        return (None, None)

