from service.base import BaseService
import os
import config
import subprocess as sp
import time
import config
from req import Service
from utils.form import form_validation

class ProblemService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        ProblemService.inst = self

    def get_problem_list(self, data={}):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+page',
            'type': int,
        }, {
            'name': '+count',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql = """
            SELECT 
            (SELECT COUNT(*) FROM (SELECT * FROM submissions WHERE problem_id=p.id AND user_id=%s AND verdict=9 limit 1) AS m) AS ac, 
            (SELECT COUNT(*) FROM (SELECT * FROM submissions WHERE problem_id=p.id AND user_id=%s limit 1) AS n) AS try, 
            p.id, p.title, p.source, p.visible, p.created_at,
            u.id as setter_user_id, u.account as setter_user,
            g.id as group_id, g.name as group_name
            FROM problems as p, users as u, groups as g
            WHERE u.id=p.setter_user_id AND g.id=p.group_id AND
            """
        sql += """ (p.group_id=%s) """
        sql += """ ORDER BY p.id limit %s OFFSET %s """

        res  = yield self.db.execute(sql, (data['user_id'], data['user_id'], data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"]), ))
        return (None, res.fetchall())
        
    ### Should be improvement
    def get_problem_list_count(self, data={}):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # res = self.rs.get('problem_list_count@%s' 
                # % (str(data['group_id'])))
        # if res: return (None, res)
        sql = "SELECT COUNT(*) FROM problems as p "
        sql += "WHERE p.group_id=%s"
        res = yield self.db.execute(sql, (data['group_id'],))
        res = res.fetchone()
        # self.rs.set('problem_list_count@%s'
                # % (str(data['group_id'])), res['count'])
        return (None, res['count'])

    def get_problem(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        if int(data['id']) == 0:
            col = ["id", "title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "group_id", "setter_user_id", "visible", "interactive", "checker_id", "created_at", "updated_at","pdf"]
            res = { x: "" for x in col }
            res['id'] = 0
            res['visible'] = 0
            res['verdict_id'] = 1
            return (None, res)

        # res = self.rs.get('problem@%s' % str(data['id']))
        res = None
        if not res:
            sql = "SELECT p.*, u.account as setter_user FROM problems as p, users as u WHERE p.setter_user_id=u.id AND p.id=%s"
            res = yield self.db.execute(sql, (data["id"], ))
            if res.rowcount == 0:
                return ('No problem id', None)
            res = res.fetchone()
            # self.rs.set('problem@%s' % str(data['id']), res)
        err, res['execute'] = yield from Service.Problem.get_problem_execute({'problem_id': data['id']})
        err, res['testdata'] = yield from Service.Testdata.get_testdata_list_by_problem({'problem_id': data['id']})
        return (None, res)

    def reset_rs_problem_count(self, group_id):
        # self.rs.delete('problem_list_count@%s' % str(group_id))
        # self.rs.delete('problem_list_count@1')
        pass

    def put_problem(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
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
            'xss': True,
        }, {
            'name': 'input',
            'type': str,
            'xss': True,
        }, {
            'name': 'output',
            'type': str,
            'xss': True,
        }, {
            'name': 'sample_input',
            'type': str,
            'xss': True,
        }, {
            'name': 'sample_output',
            'type': str,
            'xss': True,
        }, {
            'name': 'hint',
            'type': str,
            'xss': True,
        }, {
            'name': 'source',
            'type': str,
            'xss': True,
        }, {
            'name': '+visible',
            'type': int,
        }, {
            'name': '+verdict_id',
            'type': int,
        }, {
            'name': 'verdict_code',
        }, {
            'name': 'verdict_execute_type_id',
            'type': int,
        }, {
            'name': 'pdf',
            'type': bool,
        }, {
            'name': 'pdf_file',
        }, {
            'name': '+score_type_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        new_verdict = False
        verdict_code = data.pop('verdict_code')
        verdict_execute_type_id = data.pop('verdict_execute_type_id')
        if int(data['verdict_id']) == 0:
            new_verdict = True
            meta = {}
            meta['id'] = 0
            meta['title'] = 'special judge'
            meta['execute_type_id'] = verdict_execute_type_id
            meta['setter_user_id'] = data['setter_user_id']
            meta['code_file'] = verdict_code
            err, data['verdict_id'] = yield from Service.Verdict.post_verdict(meta)
            if err: return (err, None)

        pdf_file = data.pop('pdf_file')
        # if data.get('pdf'):
            # if pdf_file is None:
                # return ('pdf file should be uploaded', None)

        # self.reset_rs_problem_count(data['group_id'])
        id = data.pop('id')
        # self.rs.delete('problem@%s' % str(id))
        sql, parma = self.gen_update_sql("problems", data)
        yield self.db.execute("%s WHERE id = %s" % (sql, id), parma)
        yield self.db.execute('DELETE FROM verdicts WHERE problem_id=%s AND id!=%s;', (id, data['verdict_id'],))
        if new_verdict:
            meta['id'] = data['verdict_id']
            meta['title'] = 'special judge for problem %s'%(id)
            meta['setter_user_id'] = data['setter_user_id']
            meta['problem_id'] = id
            meta['code_file'] = None
            err, data['verdict_id'] = yield from Service.Verdict.post_verdict(meta)
            if err: return (err, None)

        if pdf_file:
            folder = '%s/data/problems/%s' % (config.DATAROOT, str(id))
            file_path = '%s/pdf.pdf' % folder
            try: os.makedirs(folder)
            except: pass
            with open(file_path, 'wb+') as f:
                f.write(pdf_file['body'])
        
        return (None, id)

    def post_problem(self, data={}):
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
            'xss': True,
        }, {
            'name': 'input',
            'type': str,
            'xss': True,
        }, {
            'name': 'output',
            'type': str,
            'xss': True,
        }, {
            'name': 'sample_input',
            'type': str,
            'xss': True,
        }, {
            'name': 'sample_output',
            'type': str,
            'xss': True,
        }, {
            'name': 'hint',
            'type': str,
            'xss': True,
        }, {
            'name': 'source',
            'type': str,
            'xss': True,
        }, {
            'name': '+visible',
            'type': int,
        }, {
            'name': '+verdict_id',
            'type': int,
        }, {
            'name': 'verdict_code',
        }, {
            'name': 'verdict_execute_type_id',
            'type': int,
        }, {
            'name': 'pdf',
            'type': bool,
        }, {
            'name': 'pdf_file',
        }, {
            'name': '+score_type_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        new_verdict = False
        verdict_code = data.pop('verdict_code')
        verdict_execute_type_id = data.pop('verdict_execute_type_id')
        if int(data['verdict_id']) == 0:
            print('verdict')
            new_verdict = True
            meta = {}
            meta['id'] = 0
            meta['title'] = 'special judge'
            meta['execute_type_id'] = verdict_execute_type_id
            meta['setter_user_id'] = data['setter_user_id']
            meta['code_file'] = verdict_code
            err, data['verdict_id'] = yield from Service.Verdict.post_verdict(meta)
            if err: return (err, None)

        pdf_file = data.pop('pdf_file')
        # if data.get('pdf'):
            # if pdf_file is None:
                # return ('pdf file should be uploaded', None)

        self.reset_rs_problem_count(data['group_id'])
        sql, parma = self.gen_insert_sql("problems", data)
        id = (yield self.db.execute(sql, parma)).fetchone()['id']
        yield from Service.Problem.put_problem_execute({
            'problem_id': id,
            'execute': [
                1, 2, 3, 4
            ]
        })
        if new_verdict:
            meta['id'] = data['verdict_id']
            meta['title'] = 'special judge for problem %s'%(id)
            meta['setter_user_id'] = data['setter_user_id']
            meta['problem_id'] = id
            meta['code_file'] = None
            err, data['verdict_id'] = yield from Service.Verdict.post_verdict(meta)
            if err: return (err, None)

        if pdf_file:
            folder = '%s/data/problems/%s' % (config.DATAROOT, str(id))
            file_path = '%s/pdf.pdf' % folder
            try: os.makedirs(folder)
            except: pass
            with open(file_path, 'wb+') as f:
                f.write(pdf_file['body'])
        
        return (None, id)

    def delete_problem(self, data={}):
        required_args = [{
            'name': 'id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        err, data = yield from self.get_problem(data)
        if err: return (err, None)
        # self.reset_rs_problem_count(data['group_id'])
        yield self.db.execute("DELETE FROM problems WHERE id=%s", (int(data['id']),))
        # self.rs.delete('problem@%s' % str(data['id']))
        # self.rs.delete('problem@%s@execute' % str(data['id']))
        return (None, None)
    
    def post_rejudge_problem(self, data={}):
        required_args = [{
            'name': 'id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('SELECT s.id FROM submissions as s WHERE s.problem_id=%s ORDER BY s.id;', (data['id'],))
        res = res.fetchall()
        # for x in res: self.rs.delete('submission@%s'%(str(x['id'])))
        yield self.db.execute('UPDATE submissions SET time_usage=%s, memory_usage=%s, score=%s, verdict=%s WHERE id IN %s;', (None, None, None, 1, tuple(x['id'] for x in res)))
        yield self.db.execute('DELETE FROM map_submission_testdata WHERE submission_id IN %s;', (tuple(x['id'] for x in res),))
        yield self.db.execute('INSERT INTO wait_submissions (submission_id) VALUES '+','.join('(%s)'%x['id'] for x in res))
        return (None, str(data['id']))

    def get_problem_execute(self, data={}):
        required_args = [{
            'name': '+problem_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # res = self.rs.get('execute@problem@%s'%str(data['problem_id']))
        # if res: return (None, res)
        res = yield self.db.execute("SELECT e.* FROM execute_types as e, map_problem_execute as m WHERE m.execute_type_id=e.id and m.problem_id=%s ORDER BY e.priority", (data['problem_id'],))
        res = res.fetchall()
        # self.rs.set('execute@problem@%s' % str(data['problem_id']), res)
        return (None, res)

    def put_problem_execute(self, data={}):
        required_args = [{
            'name': '+problem_id',
            'type': int,
        }, {
            'name': '+execute',
            'type': list,
        }, ]
        err = form_validation(data, required_args)
        if err: return (err, None)
        yield from self.delete_problem_execute(data)
        for x in data['execute']:
            try:
                yield self.db.execute("INSERT INTO map_problem_execute (execute_type_id, problem_id) values (%s, %s)", (x, data['problem_id']))
            except: pass
        return (None, data['problem_id'])

    def delete_problem_execute(self, data={}):
        required_args = [{
            'name': '+problem_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # self.rs.delete('execute@problem@%s' % str(data['problem_id']))
        yield self.db.execute("DELETE FROM map_problem_execute WHERE problem_id=%s", (data['problem_id'],))
        return (None, None)

    def post_problem_tag(self, data={}):
        required_args = [{
            'name': '+tag_id',
            'type': str,
        }, {
            'name': '+problem_id',
            'type': str,
        }]
        # err = self.check_required_args(required_args, data)
        err = form_validation(data, required_args)
        if err: return (err, None)
        # self.rs.delete('tag@problem@%s'%(data['problem_id']))
        try: yield self.db.execute('INSERT INTO map_problem_tag (tag_id, problem_id) VALUES(%s, %s);', (data['tag_id'], data['problem_id']))
        except: return ((400, 'Already in'), None)
        return (None, None)

    def delete_problem_tag(self, data={}):
        required_args = ['tag_id', 'problem_id']
        required_args = [{
            'name': '+tag_id',
            'type': str,
        }, {
            'name': '+problem_id',
            'type': str,
        }]
        # err = self.check_required_args(required_args, data)
        err = form_validation(data, required_args)
        if err: return (err, None)
        # self.rs.delete('tag@problem@%s'%(data['problem_id']))
        res = yield self.db.execute('DELETE FROM map_problem_tag WHERE tag_id=%s AND problem_id=%s RETURNING id;', (data['tag_id'], data['problem_id']))
        if res.rowcount == 0:
            return ((404, 'no this tag in this problem'), None)
        return (None, None)

    def get_problem_tag(self, data={}):
        required_args = ['problem_id']
        required_args = [{
            'name': '+problem_id',
            'type': int,
        }]
        # err = self.check_required_args(required_args, data)
        err = form_validation(data, required_args)
        if err: return (err, None)
        # res = self.rs.get('tag@problem@%s'%(str(data['problem_id'])))
        # if res: return (None, res)
        res = yield self.db.execute('SELECT t.* FROM tags as t, map_problem_tag as m WHERE m.tag_id=t.id AND m.problem_id=%s;', (data['problem_id'],))
        res = res.fetchall()
        # self.rs.set('tag@problem@%s'%(str(data['problem_id'])), res)
        return (None, res)
