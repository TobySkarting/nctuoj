from service.base import BaseService
import config

class ExecuteService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        ExecuteService.inst = self

    def get_execute_list(self, data={}):
        res = self.rs.get('execute_list')
        if res: return (None, res)
        sql = "SELECT e.*, u.account as setter_user FROM execute_types as e, users as u WHERE e.setter_user_id=u.id order by e.priority"
        res, res_cnt = yield from self.db.execute(sql)
        self.rs.set('execute_list', res)
        return (None, res)

    
    def get_execute(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['id']) == 0:
            res = {}
            res['steps'] = []
            res['id'] = 0
            res['lang'] = 0
            res['description'] = ''
            return (None, res)
        res = self.rs.get('execute@%s'%(str(data['id'])))
        if res: return (None, res)
        sql = "SELECT e.*, u.account as setter_user FROM execute_types as e, users as u WHERE e.id=%s AND e.setter_user_id=u.id"
        res, res_cnt = yield from self.db.execute(sql, (data["id"]))
        if res_cnt == 0:
            return ('Error execute id', None)
        res = res[0]
        res['steps'], res_cnt = yield from self.db.execute("SELECT execute_steps.* FROM execute_steps WHERE execute_type_id=%s ORDER BY id", (res['id'],))
        for x in range(len(res['steps'])):
            res['steps'][x]['step'] = x + 1
        self.rs.set('execute@%s'%(str(data['id'])), res)
        return (None, res)

    def post_execute(self, data={}):
        self.rs.delete('execute_list')
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        command = data.pop('command')
        print('COMMAND')
        id = None
        if int(data['id']) == 0:
            data.pop('id')
            sql, parma = self.gen_insert_sql("execute_types", data)
            id = (yield from self.db.execute(sql, parma))[0][0]['id']
        else:
            id = data.pop('id')
            sql, parma = self.gen_update_sql("execute_types", data)
            yield from self.db.execute("%s WHERE id = %s" % (sql, str(id)), parma)
        yield from self.db.execute("DELETE FROM execute_steps WHERE execute_type_id=%s", (id,))
        for x in command:
            meta = {}
            meta['command'] = x
            meta['execute_type_id'] = id
            sql, parma = self.gen_insert_sql("execute_steps", meta)
            yield from self.db.execute(sql, parma)
        return (None, id)

    def delete_execute(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        yield from self.db.execute('DELETE FROM execute_types WHERE id=%s;', (data['id'],))
        yield from self.db.execute('DELETE FROM execute_steps WHERE execute_type_id=%s;', (data['id'],))
        yield from self.db.execute('DELETE FROM map_problem_execute WHERE execute_type_id=%s;', (data['id'],))
        ### ???
        yield from self.db.execute('DELETE FROM submissions WHERE execute_type_id=%s;', (data['id'],))
        yield from self.db.execute('DELETE FROM verdicts WHERE execute_type_id=%s;', (data['id'],))
        self.rs.delete('execute@%s'%(str(data['id'])))
        self.rs.delete('execute_list')
        return (None, str(data['id']))
