import tornado
import time
import subprocess
import config
class BaseService:
    def __init__(self, db, rs):
        class FTP():
            def upload(self, local, remote):
                child = subprocess.Popen(['python3', 'ftp.py', 'upload', local, remote])
                while child.poll() is None:
                    yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 0.01)

            def download(self, remote, local):
                child = subprocess.Popen(['python3', 'ftp.py', 'download', remote, local])
                while child.poll() is None:
                    yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 0.01)
        self.ftp = FTP()
        self.db = db
        self.rs = rs

    def check_required_args(self, args, data):
        for a in args:
            if a not in data:
                return 'Error: %s should exist' % a
            if not data[a]:
                return 'Error: %s should not be empty.' % a
        return None

    def gen_insert_sql(self, tablename, data):
        '''
        tablename(str)
        data(dict)
        return sql(str), prama(tuple)
        '''
        sql1 = ''.join( ' "%s",'%col for col in data )[:-1]
        sql2 = (' %s,'*len(data))[:-1]
        prama = tuple( val for val in data.values() )
        sql = 'INSERT INTO "%s" (%s) VALUES(%s) RETURNING id;' % (tablename, sql1, sql2)
        return (sql, prama)
    
    def gen_update_sql(self, tablename, data):
        '''
        tablename(str)
        data(dict)
        return sql(str), prama(tuple)
        '''
        sql = ''.join(' "%s" = %%s,'%col for col in data)[:-1]
        prama = tuple( val for val in data.values() )
        sql = 'UPDATE "%s" SET %s '%(tablename, sql)
        return (sql, prama)

    def gen_select_sql(self, tablename, data):
        '''
        tablename(str)
        data(list)
        return sql(str)
        '''
        sql = ''.join(' "%s",'%col for col in data)[:-1]
        sql = 'SELECT "%s" FROM %s '%(sql, tablename)
        return sql
