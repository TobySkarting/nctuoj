from service.base import BaseService
from req import Service
from map import map_default_file_name
from map import map_group_power
import re
import shutil
import os
import config
import shutil
import time
import tornado

class SubmissionService(BaseService):
    def __init__(self, db, rs, ftp):
        super().__init__(db, rs, ftp)
        SubmissionService.inst = self
    
    def get_submission_list(self, data):
        required_args = ['page', 'count']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        sql = """
        SELECT s.*, u.account as user, e.lang
        FROM submissions as s, users as u, execute_types as e, problems as p
        WHERE p.id=s.problem_id AND u.id=s.user_id AND e.id=s.execute_type_id
        """
        sql += " AND p.group_id=%s  "
        if 'problem_id' in data and data['problem_id']:
            sql += "AND problem_id=%s " % (int(data['problem_id']))
        if 'user_id' in data and data['user_id']:
            sql += "AND user_id=%s " % (int(data['user_id']))
        sql += " ORDER BY s.id DESC LIMIT %s OFFSET %s"
        
        res, res_cnt = yield from self.db.execute(sql, (data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"])))
        return (None, res)

    def get_submission_list_count(self, data):
        subsql = "SELECT count(*) FROM submissions as s "
        cond = " WHERE "
        if 'problem_id' in data and data['problem_id']:
            cond += "problem_id=%s AND " % (int(data['problem_id']))
        if 'user_id' in data and data['user_id']:
            cond += "user_id=%s AND " % (int(data['user_id']))
        if cond == " WHERE ":
            cond = ""
        else:
            cond = cond[:-4]
        sql = "SELECT count(*) FROM submissions " + cond
        res, res_cnt = yield from self.db.execute(sql)
        return (None, res[0]['count'])

    def get_submission(self, data):
        #if int(data['id']) == 0:
            #return ('No Submission ID', None)

        res = self.rs.get('submission@%s'%(str(data['id'])))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("""
        SELECT s.*, e.lang as execute_lang, e.description as execute_description, u.account as submitter, p.title as problem_name, p.group_id as problem_group_id, v.abbreviation as verdict_abbreviation, v.description as verdict_description  
        FROM submissions as s, execute_types as e, users as u, problems as p, map_verdict_string as v 
        WHERE s.id=%s AND e.id=s.execute_type_id AND u.id=s.user_id AND s.problem_id=p.id AND s.verdict=v.id 
        """, (data['id'],))
        if res_cnt == 0:
            return ('No Submission ID', None)
        res = res[0]
        res['testdata'], res_cnt = yield from self.db.execute('SELECT * FROM map_submission_testdata WHERE submission_id=%s;', (data['id'],))

        folder = './../data/submissions/%s/' % str(res['id'])
        file_path = '%s/%s' % (folder, res['file_name'])
        if not os.path.isfile(file_path):
            remote_folder = './data/submissions/%s/' % str(res['id'])
            remote_path = '%s/%s' % (remote_folder, res['file_name'])
            yield from self.ftp.download(remote_path, file_path)

        with open(file_path) as f:
            res['code'] = f.read()
        res['code_line'] = len(open(file_path).readlines())
        self.rs.set('submission@%s'%(str(data['id'])), res)
        return (None, res)

    def post_submission(self, data):
        required_args = ['problem_id', 'execute_type_id', 'user_id']
        err = self.check_required_args(required_args, data)
        if err: return(err, None)
        if data['code_file'] == None and len(data['plain_code']) == 0:
            return ('No code', None)
        meta = { x: data[x] for x in required_args }
        ### check problem has execute_type
        res, res_cnt = yield from self.db.execute("SELECT * FROM map_problem_execute WHERE problem_id=%s and execute_type_id=%s", (data['problem_id'], data['execute_type_id'],))
        if res_cnt == 0:
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
        id = (yield from self.db.execute(sql, parma))[0][0]['id']
        res, res_cnt = yield from self.db.execute('SELECT id FROM testdata WHERE problem_id=%s;', (data['problem_id'],))
        for x in res:
            yield from self.db.execute('INSERT INTO map_submission_testdata (testdata_id, submission_id) VALUES(%s, %s);', (x['id'], id,))
        ### save file
        folder = './../data/submissions/%s/' % str(id)
        remote_folder = './data/submissions/%s/' % str(id)
        file_path = '%s/%s' % (folder, meta['file_name'])
        remote_path = '%s/%s' % (remote_folder, meta['file_name'])
        try: shutil.rmtree(folder)
        except: pass
        try: os.makedirs(folder)
        except: pass
        with open(file_path, 'wb+') as f:
            if data['code_file']:
                f.write(data['code_file']['body'])
            else:
                f.write(data['plain_code'].encode())
        yield from self.ftp.delete(remote_folder)
        yield from self.ftp.upload(file_path, remote_path)
        yield from self.db.execute('INSERT INTO wait_submissions (submission_id) VALUES(%s);', (id,))
        return (None, id) 

    def post_rejudge(self, data={}):
        required_args = ['id']
        err =self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('submission@%s'%(str(data['id'])))
        yield from self.db.execute('INSERT INTO wait_submissions (submission_id) VALUES(%s);', (data['id'],))
        yield from self.db.execute('UPDATE submissions SET time_usage=%s, memory_usage=%s, score=%s WHERE id=%s;', (None, None, None, data['id']))
        yield from self.db.execute('UPDATE map_submission_testdata SET time_usage=%s, memory_usage=%s WHERE submission_id=%s;', (None, None, data['id']))
        print(data['id'])
        return (None, str(data['id']))
