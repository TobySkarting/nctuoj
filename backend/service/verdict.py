from service.base import BaseService
import os
import config

class VerdictService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        VerdictService.inst = self

    def get_verdict_list(self, data={}):
        res = self.rs.get('verdict_list')
        if res: return (None, res)
        sql = "SELECT v.*, u.account as setter_user FROM verdicts as v, users as u WHERE v.setter_user_id=u.id"
        res, res_cnt = yield from self.db.execute(sql)
        self.rs.set('verdict_list', res)
        return (None, res)

    
    def get_verdict(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('verdict@%s'%str(data['id']))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT v.*, u.account as setter_user FROM verdicts as v, users as u WHERE v.id=%s AND v.setter_user_id=u.id;', (data['id'],))
        if res_cnt == 0:
            return ('No Verdict ID', None)
        res = res[0]
        err, res['execute_type'] = yield from Service.Execute.get_execute({'id': res['execute_type_id']})

        folder = './../data/verdicts/%s/' % str(res['id'])
        file_path = '%s/%s' % (folder, res['file_name'])
        if not os.path.isfile(file_path):
            remote_folder = './data/verdicts/%s/' % str(res['id'])
            remote_path = '%s/%s' % (remote_folder, res['file_name'])
            yield from self.ftp.download(remote_path, file_path)

        with open(file_path) as f:
            res['code'] = f.read()
        res['code_line'] = len(open(file_path).readlines())
        self.rs.set('verdict@%s'%(str(data['id'])), res)
        return (None, res)

    def post_verdict(self ,data={}):
        required_args = ['id', 'title', 'execute_type_id', 'setter_user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        code_file = None
        id = None
        if int(data['id']) == 0:
            if data['code_file'] is None:
                return ('No code file', None)
            data['file_name'] = data['code_file']['file_name']
            code_file = data.pop('code_file')
            data.pop('id')
            sql, param = self.gen_insert_sql('verdicts', data)
            id, res_cnt = yield from self.db.execute(sql, param)
        else:
            code_file = data.pop('code_file')
            if code_file: data['file_name'] = code_file['filename']
            sql, param = self.gen_update_sql('verdicts', data)
            id = data.pop('id')
            yield from self.db.execute(sql+' WHERE id=%s;', param+(id,))
        
        if code_file:
            folder = './../data/verdicts/%s/' % str(id)
            remote_folder = './data/verdicts/%s/' % str(id)
            file_path = '%s/%s' % (folder, data['file_name'])
            remote_path = '%s/%s' % (remote_folder, data['file_name'])
            try: shutil.rmtree(folder)
            except: pass
            try: os.makedirs(folder)
            except: pass
            with open(file_path, 'wb+') as f:
                f.write(code_file['body'])
            yield from self.ftp.upload(file_path, remote_path)
        return (None, str(id))

    def delete_verdict(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        yield from self.db.execute('DELETE FROM verdicts WHERE id=%s;', (data['id'],))
        self.rs.delete('verdict_list')
        self.rs.delete('verdict@%s'%(str(data['id'])))
        return (None, str(data['id']))


