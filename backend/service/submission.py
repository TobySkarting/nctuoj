from service.base import BaseService
from req import Service
from map import map_default_file_name
from map import map_group_power
from utils.form import form_validation
import re
import shutil
import os
import config
import shutil
import time
import tornado
import chardet

class SubmissionService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        SubmissionService.inst = self
    
    def get_submission_list(self, data):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+page',
            'type': int,
        }, {
            'name': '+count',
            'type': int,
        }, {
            'name': 'account',
            'type': str,
        }, {
            'name': 'problem_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql = """
        SELECT s.*, u.account as user, p.title as problem_title
        FROM submissions as s, users as u, problems as p
        WHERE p.id=s.problem_id AND u.id=s.user_id 
        """
        sql += " AND p.group_id=%s  "
        if data['problem_id']:
            sql += "AND problem_id=%s " % (data['problem_id'])
        if data['account']:
            try:
                user_id = (yield self.db.execute("SELECT id FROM users WHERE account=%s", (data['account'],))).fetchone()['id']
            except:
                user_id = 0
            sql += "AND user_id=%s " % (user_id)
        sql += " ORDER BY s.id DESC LIMIT %s OFFSET %s"
        res = yield self.db.execute(sql, (data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"])))
        res = res.fetchall()
        return (None, res)

    def get_submission_list_count(self, data):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }, {
            'name': 'problem_id',
            'type': int,
        }, {
            'name': 'account',
            'type': str,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql = "SELECT count(*) FROM submissions as s, problems as p"
        sql += " WHERE s.problem_id = p.id AND p.group_id=%s"%(data['group_id'])
        if data['problem_id']:
            sql += " AND problem_id=%s " % (int(data['problem_id']))
        if data['account']:
            try:
                user_id = (yield self.db.execute("SELECT id FROM users WHERE account=%s", (data['account'],))).fetchone()['id']
            except:
                user_id = 0
            sql += " AND user_id=%s " % (user_id)
        res = yield self.db.execute(sql)
        return (None, res.fetchone()['count'])

    def get_submission(self, data):
        #if int(data['id']) == 0:
            #return ('No Submission ID', None)

        #res = self.rs.get('submission@%s'%(str(data['id'])))
        #if res: return (None, res)
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("""
        SELECT s.*, u.account as submitter, p.title as problem_name, p.group_id as problem_group_id
        FROM submissions as s, users as u, problems as p
        WHERE s.id=%s AND p.group_id=%s AND u.id=s.user_id AND s.problem_id=p.id 
        """, (data['id'], data['group_id'], ))
        if res.rowcount == 0:
            return ('No Submission ID', None)
        res = res.fetchone()
        err, res['execute'] = yield from Service.Execute.get_problem_execute(res)
        res['testdata'] = yield self.db.execute('SELECT m.* FROM map_submission_testdata as m WHERE submission_id=%s ORDER BY testdata_id;', (data['id'],))
        res['testdata'] = res['testdata'].fetchall()
        folder = '/mnt/nctuoj/data/submissions/%s/' % str(res['id'])
        for x in res['testdata']:
            try: x['msg'] = open('%s/testdata_%s'%(folder, x['testdata_id'])).read()
            except: pass


        file_path = '%s/%s' % (folder, res['file_name'])
        res['code'] = open(file_path, 'rb').read()
        res['code'] = res['code'].decode(chardet.detect(res['code']))
        res['code_line'] = len(open(file_path, 'rb').readlines())
        #self.rs.set('submission@%s'%(str(data['id'])), res)
        return (None, res)

    def post_submission(self, data):
        required_args = [{
            'name': '+problem_id',
            'type': int,
        }, {
            'name': '+execute_type_id',
            'type': int,
        }, {
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+ip',
            'type': str,
        }]
        err = form_validation(data, required_args)
        if err: return(err, None)
        if data['code_file'] == None and len(data['plain_code']) == 0:
            return ('No code', None)
        meta = { x['name']: data[x['name']] for x in required_args }
        ### check problem has execute_type
        res = yield self.db.execute("SELECT * FROM map_problem_execute WHERE problem_id=%s and execute_type_id=%s", (data['problem_id'], data['execute_type_id'],))
        if res.rowcount == 0:
            return ('No execute type', None)
        err, data['execute'] = yield from Service.Execute.get_execute({'id': data['execute_type_id']})
        ### get file name and length
        if data['code_file']:
            meta['file_name'] = data['code_file']['filename']
            meta['length'] = len(data['code_file']['body'])
        else:
            if data['plain_file_name'] is None:
                data['plain_file_name'] = ''
            if re.match('[\w\.]*', data['plain_file_name']).group(0) != data['plain_file_name']:
                data['plain_file_name'] = ''
            if data['plain_file_name'] != '':
                meta['file_name'] = data['plain_file_name']
            else:
                meta['file_name'] = map_default_file_name[int(data['execute']['lang'])]
            meta['length'] = len(data['plain_code'])
        ### save to db
        sql, parma = self.gen_insert_sql("submissions", meta)
        id = (yield self.db.execute(sql, parma)).fetchone()['id']
        # res = yield self.db.execute('SELECT id FROM testdata WHERE problem_id=%s;', (data['problem_id'],))
        # res = res.fetchall()
        ### save file
        folder = '/mnt/nctuoj/data/submissions/%s/' % str(id)
        #remote_folder = '/mnt/nctuoj/data/submissions/%s/' % str(id)
        file_path = '%s/%s' % (folder, meta['file_name'])
        #remote_path = '%s/%s' % (remote_folder, meta['file_name'])
        try: shutil.rmtree(folder)
        except: pass
        try: os.makedirs(folder)
        except Exception as e: print(e)
        #yield self.ftp.delete(remote_folder)
        #shutil.rmtree(remote_folder)
        with open(file_path, 'wb+') as f:
            if data['code_file']:
                encode = chardet.detect(data['code_file']['body'])
                data['code_file']['body'] = data['code_file']['file'].decode(encode['encoding']).encode()
                f.write(data['code_file']['body'])
            else:
                f.write(data['plain_code'].encode())
        #yield self.ftp.put(file_path, remote_path)
        yield self.db.execute('INSERT INTO wait_submissions (submission_id) VALUES(%s);', (id,))
        return (None, id) 

    def post_rejudge(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # self.rs.delete('submission@%s'%(str(data['id'])))
        yield self.db.execute('INSERT INTO wait_submissions (submission_id) VALUES(%s);', (data['id'],))
        yield self.db.execute('UPDATE submissions SET time_usage=%s, memory_usage=%s, score=%s, verdict=%s WHERE id=%s;', (None, None, None, 1, data['id']))
        yield self.db.execute('DELETE FROM map_submission_testdata WHERE submission_id=%s;', (data['id'],))
        return (None, str(data['id']))
