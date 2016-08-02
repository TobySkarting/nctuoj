from req import Service
from service.base import BaseService
from utils.utils import HashPassword
from utils.utils import GenToken


class Power(BaseService):
    def get_power(self, data):
        require_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT array_agg(power) as power FROM map_group_user_power WHERE user_id=%s AND group_id=%s", (data['user_id'],data['group_id'],))
        res = res.fetchone()
        if res['power'] is None:
            res['power'] = []
        return (None, res)

    def post_power(self, data):
        require_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+power',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('map_group_user_power', data)
        res = yield self.db.execute(sql, param)
        return (None, None)
        
    def delete_power(self, data):
        require_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+power',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        res = yield self.db.execute("DELETE FROM map_group_user_power WHERE user_id=%s AND group_id=%s AND power=%s", (data['user_id'], data['group_id'], data['power'],))
        return (None, None)
