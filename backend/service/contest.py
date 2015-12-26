from service.base import BaseService
from req import Service
import os
import config
import datetime
import math
from functools import reduce
from map import *

class ContestService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        ContestService.inst = self

    def get_current_contest(self):
        res = yield self.db.execute('SELECT id FROM contests WHERE start<=%s AND %s<="end";', (datetime.datetime.now(), datetime.datetime.now(), ))
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

        res = yield self.db.execute(sql, (data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"]), ))
        return (None, res.fetchall())
        
    def get_contest_list_count(self, data={}):
        required_args = ['group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('contest_list_count@%s' 
                % (str(data['group_id'])))
        if res: return (None, res)
        sql = "SELECT COUNT(*) FROM contests as c WHERE c.group_id=%s;"
        res = yield self.db.execute(sql, (data['group_id'],))
        res = res.fetchone()
        self.rs.set('contest_list_count@%s'
                % (str(data['group_id'])), res['count'])
        return (None, res['count'])

    def get_contest(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        ### new contest
        if int(data['id']) == 0:
            col = ['id', 'group_id', 'visible', 'title', 'description', 'setter_user_id', 'type', 'freeze']
            res = { x: '' for x in col }
            col = ['register_start', 'register_end', 'start', 'end']
            res.update({ x: datetime.datetime.now() for x in col })
            res['visible'] = 0
            res['id'] = 0
            res['problem'] = []
            return (None, res)
        
        res = self.rs.get('contest@%s'%str(data['id']))
        if not res:
            res = yield self.db.execute('SELECT c.*, u.account as setter_user FROM contests as c, users as u WHERE c.setter_user_id=u.id AND c.id=%s;', (data['id'], ))
            if res.rowcount == 0:
                return ('No Contest ID', None)
            res = res.fetchone()
            self.rs.set('contest@%s'%str(data['id']), res)
        err, res['problem'] = yield from self.get_contest_problem_list(data)
        err, res['user'] = yield from self.get_contest_user(data)
        return (None, res)

    def get_contest_problem_list(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = yield self.db.execute('SELECT p.id, p.title, m.score, m.penalty FROM map_contest_problem as m, problems as p WHERE p.id=m.problem_id AND m.contest_id=%s ORDER BY m.id ASC;', (data['id'],))
        return (None, res.fetchall())

    def post_contest(self, data={}):
        required_args = ['id', 'group_id', 'setter_user_id', 'visible', 'title', 'description', 'register_start', 'register_end', 'start', 'freeze', 'end', 'type']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if not data['freeze'] or data['freeze'] == '': data['freeze'] = 0
        #try: data['freeze'] = datetime.timedelta(minutes=int(data['freeze']))
        #except: return ('freeze time error', None) 
        # if data['end'] - data['start'] < datetime.timedelta(minutes=data['freeze']):
           # return ('freeze time too long', None)
        self.rs.delete('contest_list_count@%s' 
                % (str(data['group_id'])))
        if int(data['id']) == 0:
            data.pop('id')
            sql, param = self.gen_insert_sql('contests', data)
            insert_id = (yield self.db.execute(sql, param)).fetchone()['id']
            return (None, str(insert_id))
        else:
            err, res = yield from self.get_contest(data)
            if err: return (err, None)
            data.pop('id')
            sql, param = self.gen_update_sql('contests', data)
            yield self.db.execute(sql+' WHERE id=%s AND group_id=%s;', param+(res['id'], res['group_id'],))
            self.rs.delete('contest@%s'%str(res['id']))
            return (None, res['id'])

    def post_contest_problem(self, data={}):
        required_args = ['id', 'problems', 'scores']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('contest@%sproblem'%str(data['id']))
        yield self.db.execute('DELETE FROM map_contest_problem WHERE contest_id=%s;', (data['id'],))
        for problem, score in zip(data['problems'], data['scores']):
            meta = {}
            meta['contest_id'] = data['id']
            meta['problem_id'] = problem
            meta['score'] = score
            sql, param = self.gen_insert_sql('map_contest_problem', meta)
            yield self.db.execute(sql, param)
        return (None, data['id'])

    def get_contest_submission(self, data={}):
        required_args = ['id', 'user_id', 'current_group_power', 'submission_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from self.get_contest(data)
        if err: return (err, None)
        err, submission_res = yield from Service.Submission.get_submission({'id': data['submission_id']})
        if err: return (err, None)
        if map_group_power['contest_manage'] not in data['current_group_power']:
            if int(submission_res['user_id']) != int(data['user_id']):
                return ('No Submission id', None)
        return (None, submission_res)

    def get_contest_submissions_scoreboard(self, data={}):
        '''
        0 -> pending
        1 -> ac
        -1 -> wa
        '''
        required_args = ['id', 'current_group_power']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        admin = map_group_power['contest_manage'] in data['current_group_power']
        err, res = yield from self.get_contest(data)
        start = res['start']
        end = res['end']
        freeze_time = min(end, end-datetime.timedelta(minutes=res['freeze']))
        _, map_string_verdict = yield from Service.VerdictString.get_verdict_string_map()
        sql = '''SELECT s.id, s.user_id, s.problem_id, CEIL(extract('epoch' FROM (s.created_at - c.start)) / 60) as created_at, s.verdict as t_verdict, '''  
        if not admin:
            sql += '''(CASE WHEN (s.verdict = %s OR s.created_at >= %s) THEN 0 ELSE (CASE WHEN s.verdict = %s THEN 1 ELSE -1 END) END) AS verdict '''
        else:
            sql += '''(CASE WHEN (s.verdict = %s) THEN 0 ELSE (CASE WHEN s.verdict = %s THEN 1 ELSE -1 END) END) AS verdict '''
        sql += '''FROM submissions as s, contests as c, map_contest_user as mu, map_contest_problem as mp 
        WHERE
        c.id = %s AND 
        mu.contest_id = c.id AND 
        mu.user_id = s.user_id AND 
        mp.problem_id = s.problem_id AND
        %s <= s.created_at AND 
        s.created_at <= %s ORDER BY s.id;
        '''
        submissions = yield self.db.execute(sql, (map_string_verdict['Pending']['id'],) + ((freeze_time,) if not admin else tuple()) + (map_string_verdict['AC']['id'], data['id'], start, end))
        submissions = submissions.fetchall()
        err, users = yield from self.get_contest_user(data)
        err, problems = yield from self.get_contest_problem_list(data)
        res = {
                'submissions': submissions,
                'users': users,
                'problems': problems
                }
        return (None, res)

    def get_contest_submission_list(self, data={}):
        required_args = ['id', 'user_id', 'current_group_power']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        #res = self.rs.get('contest@%s@submission'%(str(data['id'])))
        #if res: return (None, res)
        err, res = yield from self.get_contest(data)
        start = res['start']
        end = res['end']
        freeze_time = min(end, end-datetime.timedelta(minutes=res['freeze']))
        sql = """
        SELECT s.*, u.account as user, e.lang, v.abbreviation
        FROM submissions as s, users as u, execute_types as e, map_verdict_string as v, map_contest_problem as mp, map_contest_user as mu
        WHERE """;

        if map_group_power['contest_manage'] not in data['current_group_power']:
            sql += "u.id=%s AND " % (int(data['user_id']))
        sql += """
        u.id=s.user_id AND mu.user_id=u.id 
        AND mu.contest_id=%s AND mp.contest_id=mu.contest_id  
        AND mp.problem_id=s.problem_id 
        AND e.id=s.execute_type_id AND v.id=s.verdict 
        AND %s<=s.created_at AND s.created_at<=%s 
        ORDER BY s.id DESC;
        """;
        res = yield self.db.execute(sql, (res['id'], start, end,))
        res = res.fetchall()
        # map_verdict_string, map_string_verdict = yield from Service.VerdictString.get_verdict_string_map()
        # if map_group_power['contest_manage'] not in data['current_group_power'] :
            # for submission in res:
                # if submission['created_at'] >= freeze_time:
                    # submission['verdict'] = map_string_verdict['Pending']
                    # submission['abbreviation'] = 'Pending'
        return (None, res)

    def register(self, data={}):
        required_args = ['id', 'user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from Service.User.get_user_contest(data['user_id']) 
        if err: return (err, None)
        if int(data['user_id']) in res:
            return ('You have registered', None)
        yield self.db.execute('INSERT INTO map_contest_user (contest_id, user_id) VALUES(%s, %s);', (data['id'], data['user_id'],))
        self.rs.delete('contest@%s@user'%(str(data['id'])))
        return (None, str(data['id']))

    def unregister(self, data={}):
        required_args = ['id', 'user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from Service.User.get_user_contest(data['user_id']) 
        if err: return (err, None)
        if int(data['id']) not in res:
            return ('You have not registered yet', None)
        yield self.db.execute('DELETE FROM map_contest_user WHERE contest_id=%s AND user_id=%s;', (data['id'], data['user_id'],))
        self.rs.delete('contest@%s@user'%(str(data['id'])))
        return (None, str(data['id']))

    def delete_contest(self, data={}):
        required_args = ['id', 'group_id']
        err, res = yield from self.get_contest(data)
        if err: return (err, None)
        yield self.db.execute('DELETE FROM contests WHERE id=%s;', (res['id'],))
        self.rs.delete('contest@%s'%str(res['id']))
        self.rs.delete('contest@%s@problem'%str(res['id']))
        return (None, None)

    def get_contest_user(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args , data)
        if err: return (err, None)
        res = self.rs.get('contest@%s@user'%(str(data['id'])))
        if res: return (None, res)
        res = yield self.db.execute('SELECT u.id, u.account, u.name  FROM users AS u, map_contest_user AS m WHERE m.contest_id=%s AND u.id = m.user_id;', (data['id'],))
        res = res.fetchall()
        self.rs.set('contest@%s@user'%(str(data['id'])), res)
        return (None, res)

    def get_contest_user_problem_score(self, data={}):
        required_args = ['user_id', 'problem', 'start', 'end']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = yield self.db.execute('SELECT COUNT(*) FROM submissions WHERE user_id=%s AND problem_id=%s AND %s<=created_at AND created_at<=%s;', (data['user_id'], data['problem']['id'], data['start'], data['end']))
        res = res.fetchone()
        if res['count'] == 0: ### not submit yet
            res = {}
            res['score'] = None
            res['verdict'] = 0
            res['submitted'] = 0
            res['penalty'] = 0
            return (None, res)
        res = yield self.db.execute('SELECT * FROM submissions WHERE user_id=%s AND problem_id=%s AND %s<=created_at AND created_at<=%s AND verdict=7 ORDER BY id LIMIT 1;', (data['user_id'], data['problem']['id'], data['start'], data['end']))
        if res.rowcount != 0:
            res = res.fetchone()
            data['end'] = min(data['end'], res['created_at'])
        res = yield self.db.execute('SELECT verdict, COUNT(*) as submitted, MAX(s.score) as score FROM (SELECT FROM submissions WHERE s.user_id=%s AND s.problem_id=%s AND %s<=s.created_at AND s.created_at<=%s) as s, (SELECT m.id FROM map_verdict_string as m WHERE m.priority=(SELECT MAX(m.priority) FROM map_verdict_string as m WHERE m.id=s.verdict)) as verdict;', (data['user_id'], data['problem']['id'], data['start'], data['end']))
        res = res.fetchone()
        res['penalty'] = (res['submitted']-1) * data['problem']['penalty']  
        if score != '':
            pass
        return (None, res)

    def get_contest_scoreboard(self, data={}):
        '''
        res = {
            'score': {
                'user': [
                    {
                        'id': integer,
                        'total': {
                            'penalty': integer,
                            'ac_submitted': integer,
                            'submitted': integer,
                            'score': integer,
                        }
                        'problem': {
                            problem_id(integer): {
                                'score': integer,
                                'penalty': integer,
                                'submitted': integer
                            } 
                        }
                    } 
                ]
                'problem': {
                    problem_id(integer): {
                        'total': {
                            'score': integer
                            'submitted': integer,
                            'ac_submitted': integer,
                        }
                    }
                }
            }
            'contest': contest_info(dict)
        }
        '''
        required_args = ['id']
        err = self.check_required_args(required_args , data)
        if err: return (err, None)
        start, end = data['start'], data['end']
        err, data = yield from self.get_contest(data)
        if err: return (err, None)
        start = start or data['start']
        end = end or data['end']
        if data.get('admin'):
            end = min(end, data['end']-datetime.timedelta(minutes=data['freeze']))
        res = {}
        score = res['score'] = {}
        res['contest'] = data
        res['start'] = start
        res['end'] = end
        user_score = score['user'] = []
        map_verdict_string, map_string_verdict = yield from Service.VerdictString.get_verdict_string_map()
        for user in data['user']:
            user_meta = {}
            user_meta['id'] = int(user['id'])
            user_problem = user_meta['problem'] = {}
            for problem in data['problem']:
                problem_meta = {}
                problem_meta['problem'] = problem
                problem_meta['start'] = start
                problem_meta['end'] = end
                problem_meta['user_id'] = user['id']
                err, user_problem[int(problem['id'])] = yield from self.get_contest_user_problem_score(problem_meta)
                if err: return (err, None)
            user_total = user_meta['total'] = {}
            user_total['submitted'] = sum(x['submitted'] for x in user_problem.values())
            user_total['score'] = sum(x['score'] or 0 for x in user_problem.values())
            user_total['penalty'] = sum(x['penalty'] for x in user_problem.values())
            user_total['ac_submitted'] = reduce(lambda s, x: s+(1 if x['verdict']==map_string_verdict['AC'] else 0), user_problem.values(), 0)
            user_score.append(user_meta)

        problem_score = score['problem'] = {}
        for problem in data['problem']:
            problem_total = problem_score[int(problem['id'])] = {}
            problem_total['score'] = sum(x['problem'][int(problem['id'])]['score'] or 0 for x in user_score)
            problem_total['submitted'] = sum(x['problem'][int(problem['id'])]['submitted'] for x in user_score)
            problem_total['ac_submitted'] = reduce(lambda s, x: s+(1 if x['problem'][int(problem['id'])]['verdict']==7 else 0), user_score, 0)
        
        return (None, res)



