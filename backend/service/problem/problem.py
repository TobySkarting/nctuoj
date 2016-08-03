from req import Service
from service.base import BaseService
from utils.utils import HashPassword
from utils.utils import GenToken


class Problem(BaseService):
    def get_problem(self, data):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM problems WHERE id=%s", (data['id'],))
        res = res.fetchone()
        return (None, res)

    def post_problem(self, data):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }, {
            'name': 'title',
            'type': str,
        }, {
            'name': 'description',
            'type': str,
        }, {
            'name': 'input',
            'type': str,
        }, {
            'name': 'output',
            'type': str,
        }, {
            'name': 'sample_input',
            'type': str,
        }, {
            'name': 'sample_output',
            'type': str,
        }, {
            'name': 'hint',
            'type': str,
        }, {
            'name': 'source',
            'type': str,
        }, {
            'name': 'visible',
            'type': int,
        }, {
            'name': 'score_type_id',
            'type': int,
        }]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('problems', data)
        res = yield self.db.execute(sql, param)
        res = res.fetchone()
        return (None, res)

    def put_problem(self, data):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }, {
            'name': 'title',
            'type': str,
        }, {
            'name': 'description',
            'type': str,
        }, {
            'name': 'input',
            'type': str,
        }, {
            'name': 'output',
            'type': str,
        }, {
            'name': 'sample_input',
            'type': str,
        }, {
            'name': 'sample_output',
            'type': str,
        }, {
            'name': 'hint',
            'type': str,
        }, {
            'name': 'source',
            'type': str,
        }, {
            'name': 'visible',
            'type': int,
        }, {
            'name': 'score_type_id',
            'type': int,
        }]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        id = data.pop('id')
        sql, param = self.gen_update_sql('problems', data)
        yield self.db.execute(sql + " WHERE id=%s", param + (id,))
        return (None, None)

    def delete_problem(self, data):
        required_args = [{
            'name': '+id',
            'type': int,
        },]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        yield self.db.execute("DELETE FROM problems WHERE id=%s", (data['id'],))
        return (None, None)

