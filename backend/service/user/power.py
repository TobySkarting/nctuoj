from req import Service
from service.base import BaseService
from utils.utils import HashPassword
from utils.utils import GenToken


class Power(BaseService):
    def get_power(self, data):
        required_args = [{
            'name': '+user_id',
            'type': int,
        },]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT array_agg(power) as power FROM map_user_power WHERE user_id=%s", (data['user_id'],))
        res = res.fetchone()
        if res['power'] is None:
            res['power'] = []
        return (None, res)

    def post_power(self, data):
        required_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+power',
            'type': int,
        },]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('map_user_power', data)
        res = yield self.db.execute(sql, param)
        return (None, None)
        
    def delete_power(self, data):
        required_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+power',
            'type': int,
        },]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("DELETE FROM map_user_power WHERE user_id=%s AND power=%s", (data['user_id'], data['power'],))
        return (None, None)
