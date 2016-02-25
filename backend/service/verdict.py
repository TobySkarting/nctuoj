from service.base import BaseService
from req import Service
from utils.form import form_validation
import os
import config

class VerdictService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        VerdictService.inst = self

    def get_verdict_list(self, data={}):
        # res = self.rs.get('verdict_list')
        # if res: return (None, res)
        required_args = [{
            'name': 'problem_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql = "SELECT v.*, u.account as setter_user FROM verdicts as v, users as u WHERE v.setter_user_id=u.id"
        param = tuple()
        if 'problem_id' in data and data['problem_id']:
            sql += ' AND (v.problem_id=%s OR v.problem_id=0)'
            param = (data['problem_id'],)
        res = yield self.db.execute(sql, param)
        res = res.fetchall()
        # self.rs.set('verdict_list', res)
        return (None, res)

    def get_verdict_type(self):
        # res = self.rs.get('verdict_type')
        # if res: return (None, res)
        res = { x['id']: x for x in (yield self.db.execute("SELECT * FROM map_verdict_string order by id"))}
        # self.rs.set('verdict_type', res)
        return (None, res)
    
    def get_verdict(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        if int(data['id']) == 0:
            col = ['id', 'title', 'execute_type_id', 'execute_type_id', 'file_name', 'setter_user_id']
            res = {x: '' for x in col}
            res['id'] = 0
            return (None, res)
        # res = self.rs.get('verdict@%s'%str(data['id']))
        # if res: return (None, res)
        res = yield self.db.execute('SELECT v.*, u.account as setter_user FROM verdicts as v, users as u WHERE v.id=%s AND v.setter_user_id=u.id;', (data['id'],))
        if res.rowcount == 0:
            return ((404, 'No Verdict ID'), None)
        res = res.fetchone()
        err, res['execute_type'] = yield from Service.Execute.get_execute({'id': res['execute_type_id']})

        folder = '/mnt/nctuoj/data/verdicts/%s/' % str(res['id'])
        file_path = '%s/%s' % (folder, res['file_name'])
        try: os.makedirs(folder)
        except: pass
        with open(file_path) as f:
            res['code'] = f.read()
        res['code_line'] = len(open(file_path).readlines())
        # self.rs.set('verdict@%s'%(str(data['id'])), res)
        return (None, res)

    def post_verdict(self ,data={}):
        required_args = [{
            'name': '+title',
            'type': str,
        }, {
            'name': '+execute_type_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }, {
            'name': 'code_file',
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        code_file = None
        if data['code_file'] is None:
            return ('No code file', None)
        data['file_name'] = data['code_file']['filename']
        code_file = data.pop('code_file')
        sql, param = self.gen_insert_sql('verdicts', data)
        id = (yield self.db.execute(sql, param)).fetchone()['id']
        
        if code_file:
            folder = '/mnt/nctuoj/data/verdicts/%s/' % str(id)
            file_path = '%s/%s' % (folder, data['file_name'])
            try: shutil.rmtree(folder)
            except: pass
            try: os.makedirs(folder)
            except: pass
            with open(file_path, 'wb+') as f:
                f.write(code_file['body'])
        # self.rs.delete('verdict@%s'%(str(id)))
        # self.rs.delete('verdict_list')
        return (None, str(id))

    def put_verdict(self ,data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+title',
            'type': str,
        }, {
            'name': '+execute_type_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }, {
            'name': 'code_file',
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        code_file = data.pop('code_file')
        if code_file: data['file_name'] = code_file['filename']
        sql, param = self.gen_update_sql('verdicts', data)
        id = data.pop('id')
        yield self.db.execute(sql+' WHERE id=%s;', param+(id,))
        
        if code_file:
            folder = '/mnt/nctuoj/data/verdicts/%s/' % str(id)
            file_path = '%s/%s' % (folder, data['file_name'])
            try: shutil.rmtree(folder)
            except: pass
            try: os.makedirs(folder)
            except: pass
            with open(file_path, 'wb+') as f:
                f.write(code_file['body'])
        # self.rs.delete('verdict@%s'%(str(id)))
        # self.rs.delete('verdict_list')
        return (None, str(id))

    def delete_verdict(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        yield self.db.execute('DELETE FROM verdicts WHERE id=%s;', (data['id'],))
        # self.rs.delete('verdict_list')
        # self.rs.delete('verdict@%s'%(str(data['id'])))
        return (None, str(data['id']))


