from service.base import BaseService
from req import Service
import os
import config
import datetime

class ContestService(BaseService):
    def __init__(self, db, rs, ftp):
        super().__init__(db, rs, ftp)
        ContestService.inst = self

    def get_current_contest(self):
        res, res_cnt = yield from self.db.execute('SELECT id FROM contests WHERE start<=%s AND %s<="end";', (datetime.datetime.now(), datetime.datetime.now(), ))
        return (None, list(set(int(x['id']) for x in res)))

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
        sql = "SELECT COUNT(*) FROM contests as c WHERE c.group_id=%s;"
        res, res_cnt = yield from self.db.execute(sql, (data['group_id'],))
        self.rs.set('contest_list_count@%s'
                % (str(data['group_id'])), res[0]['count'])
        return (None, res[0]['count'])

    def get_contest(self, data={}):
        required_args = ['id']
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
            res['problem'] = []
            return (None, res)
        
        res = self.rs.get('contest@%s'%str(data['id']))
        if not res:
            res, res_cnt = yield from self.db.execute('SELECT c.*, u.account as setter_user FROM contests as c, users as u WHERE c.setter_user_id=u.id AND c.id=%s;', (data['id'], ))
            if res_cnt == 0:
                return ('No Contest ID', None)
            res = res[0]
            self.rs.set('contest@%s'%str(data['id']), res)
        err, res['problem'] = yield from self.get_contest_problem_list(data)
        err, res['user'] = yield from self.get_contest_user(data)
        return (None, res)

    def get_contest_problem_list(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute('SELECT p.id, p.title, m.score FROM map_contest_problem as m, problems as p WHERE p.id=m.problem_id AND m.contest_id=%s ORDER BY m.id ASC;', (data['id'],))
        return (None, res)

    def post_contest(self, data={}):
        required_args = ['id', 'group_id', 'setter_user_id', 'visible', 'title', 'description', 'register_start', 'register_end', 'start', 'end', 'type']
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
            return (None, res['id'])

    def post_contest_problem(self, data={}):
        required_args = ['id', 'problems', 'scores']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('contest@%sproblem'%str(data['id']))
        yield from self.db.execute('DELETE FROM map_contest_problem WHERE contest_id=%s;', (data['id'],))
        for problem, score in zip(data['problems'], data['scores']):
            meta = {}
            meta['contest_id'] = data['id']
            meta['problem_id'] = problem
            meta['score'] = score
            sql, param = self.gen_insert_sql('map_contest_problem', meta)
            yield from self.db.execute(sql, param)
        return (None, data['id'])

    def get_contest_submission(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('contest@%ssubmission'%(str(data['id'])))
        if res: return (None, res)
        err, res = yield from self.get_contest(data)
        if err: return (err, None)
        end = res['end']
        res, res_cnt = yield from self.db.execute('SELECT s.* FROM submissions as s, (SELECT m.user_id FROM map_contest_user as m WHERE m.contest_id=%s) as u WHERE s.user_id=u.user_id AND %s<=s.created_at AND s.created_at<=%s ORDER BY s.id ASC;', (res['id'], res['start'], res['end'],))
        if datetime.datetime.now() > end:
            self.rs.set('contest@%ssubmission'%(str(data['id'])), res)
        return (None, res)

    def register(self, data={}):
        required_args = ['id', 'user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from Service.User.get_user_contest(data['user_id']) 
        if err: return (err, None)
        if int(data['user_id']) in res:
            return ('You have registered', None)
        yield from self.db.execute('INSERT INTO map_contest_user (contest_id, user_id) VALUES(%s, %s);', (data['id'], data['user_id'],))
        self.rs.delete('contest@%s@user'%(str(data['id'])))
        return (None, str(data['id']))

    def unregister(self, data={}):
        required_args = ['id', 'user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from Service.User.get_user_contest(data['user_id']) 
        if err: return (err, None)
        if int(data['user_id']) not in res:
            return ('You have not registered yet', None)
        yield from self.db.execute('DELETE FROM map_contest_user WHERE contest_id=%s AND user_id=%s;', (data['id'], data['user_id'],))
        self.rs.delete('contest@%s@user'%(str(data['id'])))
        return (None, str(data['id']))

    def delete_contest(self, data={}):
        required_args = ['id', 'group_id']
        err, res = yield from self.get_contest(data)
        if err: return (err, None)
        yield from self.db.execute('DELETE FROM contests WHERE id=%s;', (res['id'],))
        self.rs.delete('contest@%s'%str(res['id']))
        self.rs.delete('contest@%s@problem'%str(res['id']))
        return (None, None)

    def get_contest_user(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args , data)
        if err: return (err, None)
        res = self.rs.get('contest@%s@user'%(str(data['id'])))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT * FROM map_contest_user WHERE contest_id=%s;', (data['id'],))
        self.rs.set('contest@%s@user'%(str(data['id'])), res)
        return (None, res)

    def get_contest_scoreboard(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args , data)
        if err: return (err, None)
        err, data = yield from self.get_contest(data)


