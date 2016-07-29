from req import Service
from service.base import BaseService
from utils.utils import HashPassword
from utils.utils import GenToken


class Group(BaseService):
    def get_group(self, data):
        require_args = [{
            'name': '+id',
            'type': int,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        self.log(data)
        res = yield self.db.execute("SELECT * FROM groups WHERE id=%s", (data['id'],))
        res = res.fetchone()
        return (None, res)

    def post_group(self, data):
        require_args = [{
            'name': '+name',
            'type': str,
        }, {
            'name': '+description',
            'type': str,
        }, {
            'name': '+type',
            'type': int,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('groups', data)
        res = yield self.db.execute(sql, param)
        res = res.fetchone()
        return (None, res)

    def put_group(self, data):
        require_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+name',
            'type': str,
        }, {
            'name': '+description',
            'type': str,
        }, {
            'name': '+type',
            'type': int,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        id = data.pop('id')
        sql, param = self.gen_update_sql('groups', data)
        yield self.db.execute(sql + " WHERE id=%s", param + (id,))
        return (None, None)

    def delete_group(self, data):
        require_args = [{
            'name': '+id',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        yield self.db.execute("DELETE FROM groups WHERE id=%s", (data['id'],))
        return (None, None)

