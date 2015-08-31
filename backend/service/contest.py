from service.base import BaseService
from req import Service
import os
import config
import datetime

class ContestService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        ContestService.inst = self

    def get_contest_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        sql = """
            SELECT 
            c.*,
            u.id as setter_user_id, u.account as setter_user,
            g.id as group_id, g.name as group_name
            FROM contests as c, users as u, groups as g
            WHERE u.id=c.setter_user_id AND g.id=c.group_id AND
            """
        if int(data['group_id']) == 1:
            sql += " (c.group_id=%s OR c.visible=2) "
        else:
            sql += " (c.group_id=%s) "
        sql += " ORDER BY c.id limit %s OFFSET %s "

        res, res_cnt = yield from self.db.execute(sql, (data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"]), ))
        return (None, res)
        
    def get_contest_list_count(self, data={}):
        required_args = ['group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('contest_list_count@%s' 
                % (str(data['group_id'])))
        if res: return (None, res)
        sql = "SELECT COUNT(*) FROM contests as c "
        if int(data['group_id']) == 1:
            sql += "WHERE (c.group_id=%s OR c.visible = 2)"
        else:
            sql += "WHERE c.group_id=%s"
        res, res_cnt = yield from self.db.execute(sql, (data['group_id'],))
        self.rs.set('contest_list_count@%s'
                % (str(data['group_id'])), res[0]['count'])
        return (None, res[0]['count'])

    def get_contest(self, data={}):
        required_args = ['id', 'group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        ### new contest
        if int(data['id']) == 0:
            col = ['id', 'group_id', 'visible', 'title', 'description', 'setter_user_id', 'type']
            res = { x: '' for x in col }
            col = ['register_start', 'register_end', 'start', 'end']
            res.update({ x: datetime.datetime.now() for x in col })
            res['visible'] = 0
            res['id'] = 0
            return (None, res)
        
        res = self.rs.get('contest@%s'%str(data['id']))
        if not res:
            res, res_cnt = yield from self.db.execute('SELECT c.*, u.account as setter_user FROM contests as c, users as u WHERE c.setter_user_id=u.id AND c.id=%s AND c.group_id=%s;', (data['id'], data['group_id'],))
            if res_cnt == 0:
                return ('No Contest ID', None)
            res = res[0]
            self.rs.set('contest@%s'%str(data['id']), res)
        err, res['problem'] = yield from self.get_contest_problem_list(data)
        return (None, res)

    def get_contest_problem_list(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('contest@%s@problem'%str(data['id']))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("""
        SELECT p.id, p.title FROM 
        map_contest_problem as m, problems as p
        WHERE p.id=m.problem_id and m.contest_id=%s;
        """, (data['id'],))
        self.rs.set('contest@%s@problem'%str(data['id']), res)
        return (None, res)

    def post_contest(self, data={}):
        required_args = ['id', 'group_id', 'visible', 'setter_user_id', 'title', 'description', 'register_start', 'register_end', 'start', 'end', 'type']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('contest_list_count@%s' 
                % (str(data['group_id'])))
        if int(data['id']) == 0:
            data.pop('id')
            sql, param = self.gen_insert_sql('contests', data)
            insert_id = (yield from self.db.execute(sql, param))[0][0]['id']
            return (None, str(insert_id))
        else:
            err, res = yield from self.get_contest(data)
            if err: return (err, None)
            data.pop('id')
            sql, param = self.gen_update_sql('contests', data)
            yield from self.db.execute(sql+' WHERE id=%s AND group_id=%s;', param+(res['id'], res['group_id'],))
            self.rs.delete('contest@%s'%str(res['id']))
            return (None, None)

    def post_contest_problem(self, data={}):
        required_args = ['id', 'contest_id', 'problem_id', 'score']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from Service.Problem.get_problem({'id': data['problem_id'], 'group_id': data['group_id']})
        if err: return (err, None)
        self.rs.delete('contest@%s@problem'%str(data['contest_id']))
        data['score'] = int(data['score']) if data['score'] != '' else 100
        if int(data['id']) == 0:
            data.pop('id')
            sql, param = self.gen_insert_sql('map_contest_problem', data)
            insert_id = (yield from self.db.execute(sql, param))[0][0]['id']
            return (None, str(insert_id))
        else:
            sql, param = self.gen_update_sql('map_contest_problem', data)
            yield from self.db.execute(sql+' WHERE id=%s;', param+(data['id'],))
            return (None, None)

    def delete_contest_problem(self, data):
        required_args = ['id', 'contest_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('contest@%s@problem'%str(data['contest_id']))
        yield from self.db.execute('DELETE FROM map_contest_problem WHERE id=%s;', (data['id'],))
        return (None, None)

    def delete_contest(self, data={}):
        required_args = ['id', 'group_id']
        err, res = yield from self.get_contest(data)
        if err: return (err, None)
        yield from self.db.execute('DELETE FROM contests WHERE id=%s;', (res['id'],))
        yield from self.db.execute('DELETE FROM map_contest_problem WHERE contest_id=%s;', (res['id'],))
        self.rs.delete('contest@%s'%str(res['id']))
        self.rs.delete('contest@%s@problem'%str(res['id']))
        return (None, None)
