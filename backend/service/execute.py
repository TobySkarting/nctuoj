from service.base import BaseService
import config

class ExecuteService(BaseService):
    def __init__(self, db, rs, ftp):
        super().__init__(db, rs, ftp)

        ExecuteService.inst = self

    def get_execute_list(self, data={}):
        res = self.rs.get('execute_list')
        if res: return (None, res)
        sql = "SELECT e.*, u.account as setter_user FROM execute_types as e, users as u WHERE e.setter_user_id=u.id ORDER BY e.priority"
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
        res, res_cnt = yield from self.db.execute(sql, (data["id"], ))
        if res_cnt == 0:
            return ('Error execute id', None)
        res = res[0]
        res['steps'], res_cnt = yield from self.db.execute("SELECT execute_steps.* FROM execute_steps WHERE execute_type_id=%s ORDER BY id", (res['id'],))
        for id, x in enumerate(res['steps']):
            x['step'] = id + 1
        self.rs.set('execute@%s'%(str(data['id'])), res)
        return (None, res)

    def post_execute(self, data={}):
        self.rs.delete('execute_list')
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        command = data.pop('command')
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
        self.rs.delete('execute@%s'%(str(id)))
        return (None, id)

    def post_execute_priority(self, data={}):
        required_args = ['priority']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        priority = data['priority']
        err, execute_list = yield from self.get_execute_list()
        execute_list = [x['id'] for x in execute_list]
        max_priority = len(execute_list)
        for execute in execute_list:
            execute = int(execute)
            if execute not in priority:
                return ('priority of execute_type.%s not found'%(str(execute)), None)
        id = list(priority.keys())
        for execute in priority:
            execute = int(execute)
            if execute not in execute_list:
                return ('execute_type.%s not exist'%(str(execute)), None)
            if execute > max_priority:
                return ('priority of execute_type.%s error'%(str(execute)), None)
            if id.count(execute) > 1:
                return ('priority can not duplicate', None)
        for id, pri in priority.items():
            yield from self.db.execute('UPDATE execute_types SET priority=%s WHERE id=%s;', (pri, id,))
            self.rs.delete('execute@%s'%(str(id)))
        self.rs.delete('execute_list')
        return (None, None)

    def delete_execute(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        yield from self.db.execute('DELETE FROM execute_types WHERE id=%s;', (data['id'],))
        ### ???
        self.rs.delete('execute@%s'%(str(data['id'])))
        self.rs.delete('execute_list')
        return (None, str(data['id']))
