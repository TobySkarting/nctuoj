from req import Service
from service.base import BaseService
from map import *
import os

class TestdataSerivce(BaseService):
    def __init__(self, db, rs, ftp):
        super().__init__(db, rs, ftp)
        TestdataSerivce.inst = self

    def get_testdata_list(self):
        pass

    def get_testdata_list_by_problem(self, data={}):
        required_args = ['problem_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('testdata_list@problem@%s'%(str(data['problem_id'])))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT t.* FROM testdata as t, (SELECT id FROM testdata WHERE problem_id=%s ORDER BY id ASC) as t2 where t.id=t2.id;", (data['problem_id'],))
        self.rs.set('testdata_list@problem@%s'%(str(data['problem_id'])), res)
        return (None, res)

    def get_testdata(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('testdata@%s'%(str(data['id'])))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT * FROM testdata WHERE id=%s", (data['id'], ))
        if res_cnt == 0:
            return ('No tetsdata ID', None)
        res = res[0]
        self.rs.set('testdata@%s'%(str(data['id'])), res)
        return (None, res)

    def get_testdata_by_problem(self, data={}):
        pass

    def post_testdata(self, data={}):
        required_args = ['id', 'problem_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('testdata@%s'%(str(data['id'])))
        self.rs.delete('testdata_list@problem@%s'%(str(data['problem_id'])))
        if int(data['id']) == 0:
            res, cnt = yield from self.db.execute("INSERT INTO testdata (problem_id) VALUES (%s) RETURNING id;", (data['problem_id'],))
            id = res[0]['id']
            print('ID', id)
            folder = "../data/testdata/%s/" % id
            remote_folder = "./data/testdata/%s/" % id
            try: os.makedirs(folder)
            except: pass
            for x in ['input', 'output']:
                file_path = "%s/%s" % (folder, x)
                with open(file_path, 'wb+') as f:
                    f.write(''.encode())
                remote_path = "%s/%s" % (remote_folder, x)
                print(file_path, remote_path)
                yield self.ftp.put(file_path, remote_path)
            return (None, id)
        else:
            required_args = ['time_limit', 'memory_limit', 'output_limit', 'score']
            err = self.check_required_args(required_args, data)
            if err: return (err, None)
            meta = { x: data[x] for x in required_args }
            sql, parma = self.gen_update_sql("testdata", meta)
            yield from self.db.execute("%s WHERE id=%s" % (sql, data['id']), parma)

            """ create folder """
            folder = "../data/testdata/%s" % data['id']
            print('FOLDER ', folder)
            remote_folder = "./data/testdata/%s" % data['id']
            try: os.makedirs(folder)
            except Exception as e: print(e)

            """ save file and upload to ftp """
            for x in ['input', 'output']:
                if data[x] != None:
                    file_path = "%s/%s" % (folder, x)
                    with open(file_path, 'wb+') as f:
                        f.write(data[x]['body'])
                    remote_path = "%s/%s" % (remote_folder, x)
                    yield self.ftp.put(file_path, remote_path)
            return (None, data['id'])

    def delete_testdata(self, data={}):
        required_args = ['id', 'problem_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('testdata@%s'%(str(data['id'])))
        self.rs.delete('testdata_list@problem@%s'%(data['problem_id']))
        yield from self.db.execute("DELETE FROM testdata WHERE id=%s", (data['id'],))
        return (None, None)

