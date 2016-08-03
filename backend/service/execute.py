from req import Service
from service.base import BaseService


class Execute(BaseService):
    def get_execute_list(self):
        res = yield self.db.execute("SELECT * FROM execute_types ORDER BY priority")
        res = res.fetchall()
        if res is None:
            res = []
        return (None, res)

    def get_execute(self, data={}):
        require_args = [{
            'name': '+id',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM execute_types WHERE id=%s", (data['id'],))
        res = res.fetchone()
        return (None, res)

    def get_execute_with_steps(self, data={}):
        require_args = [{
            'name': '+id',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM execute_types WHERE id=%s", (data['id'],))
        res = res.fetchone()
        commands = yield self.db.execute("SELECT es.command FROM execute_steps as es WHERE es.execute_type_id=%s ORDER BY es.id", (data['id'],))
        commands = commands.fetchall()
        if commands is None:
            commands = []
        res['commands'] = commands
        return (None, res)

    def post_execute(self, data):
        require_args = [{
            'name': '+commands',
            'type': list,
        }, {
            'name': '+description',
            'type': str,
        }, {
            'name': '+file_name',
            'type': str,
        }, {
            'name': '+language_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None) 
        commands = data.pop("commands")
        sql, param = self.gen_insert_sql('execute_types', data)
        res = yield self.db.execute(sql, param)
        res = res.fetchone()
        for x in commands:
            data = {}
            data['execute_type_id'] = res['id']
            data['command'] = x
            sql, param = self.gen_insert_sql('execute_steps', data)
            yield self.db.execute(sql, param)
        return (None, res)

    def put_execute(self, data={}):
        require_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+commands',
            'type': list,
        }, {
            'name': '+description',
            'type': str,
        }, {
            'name': '+file_name',
            'type': str,
        }, {
            'name': '+language_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }]
        err = self.form_validation(data, require_args)
        if err: return (err, None) 
        commands = data.pop("commands")
        id = data.pop('id')
        sql, param = self.gen_update_sql('execute_types', data)
        res = yield self.db.execute(sql + " WHERE id=%s", param+(id,))
        yield self.db.execute("DELETE FROM execute_steps WHERE execute_type_id=%s", (id,))
        for x in commands:
            data = {}
            data['execute_type_id'] = id
            data['command'] = x
            sql, param = self.gen_insert_sql('execute_steps', data)
            yield self.db.execute(sql, param)
        return (None, res)

    def delete_execute(self, data={}):
        require_args = [{
            'name': '+id',
            'type': int,
        },]
        err = self.form_validation(data, require_args)
        yield self.db.execute("DELETE FROM execute_types WHERE id=%s", (data['id'],))
        return (None, None)
