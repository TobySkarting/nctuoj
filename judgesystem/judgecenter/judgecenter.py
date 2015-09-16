### http://www.binarytides.com/python-socket-server-code-example/
import os
import socket
import select
import config
import psycopg2
import psycopg2.extras
import ftp
import sys
import json
import time
from myredis import MyRedis
from map import *
import datetime

SOCK_AVAILABLE_CMD = ['token', 'type', 'judged']
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class JudgeCenter:
    def __init__(self):
        self.rs = MyRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db)
        self.db = psycopg2.connect( host=config.db_host, dbname=config.db_dbname, user=config.db_user, password=config.db_password) 
        self.db.autocommit = True
        # self.ftp = ftp.FTP(config.ftp_server, config.ftp_port, config.ftp_user, config.ftp_password)

        self.recv_buffer_len = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.s.setblocking(0)
        self.s.bind((config.judgecenter_host, config.judgecenter_port))
        self.s.listen(config.judgecenter_listen)
        self.pool = [sys.stdin, self.s]
        self.client_pool = []
        self.recv_buffer_len = 1024
        self.submission_queue = []

        self.client = {}

    def cursor(self):
        return self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    class CLIENT():
        def __init__(self, addr):
            self.type = map_sock_type['unauth']
            self.addr = addr
            self.lock = 0
       
    def receive(self, sock):
        try:
            data = sock.recv(self.recv_buffer_len).decode()
            if data == '':
                raise socket.error
            res = json.loads(data)
        except socket.error:
            res = None
            self.close_socket(sock)
        except Exception as e:
            res = None
            print(data, type(data))
            print(e, 'receive msg error')
        if res and ('cmd' not in res or 'msg' not in res):
            res = None
        return res

    def check_submission_meta(self, msg):
        if 'submission_id' not in msg or 'testdata' not in msg:
            return False
        for testdata in msg['testdata']:
            if 'id' not in testdata or 'time_usage' not in testdata or 'memory_usage' not in testdata or 'verdict' not in testdata:
                return False
            try:
                testdata['id'] = int(testdata['id'])
                testdata['time_usage'] = int(testdata['time_usage'])
                testdata['memory_usage'] = int(testdata['memory_usage'])
                testdata['verdict'] = int(testdata['verdict'])
            except Exception as e:
                return False
        return True

    def gen_submission_meta(self, submission_id):
        res = {}
        res['cmd'] = 'judge'
        msg = res['msg'] = {}
        msg['submission_id'] = submission_id
        cur = self.cursor()
        cur.execute('SELECT s.problem_id, p.verdict_id, s.execute_type_id FROM submissions as s, problems as p WHERE s.id=%s;', (submission_id,))
        msg.update(cur.fetchone())
        cur.execute('SELECT * FROM execute_types WHERE id=%s;', (msg['execute_type_id'],))
        msg['execute_type'] = cur.fetchone()
        cur.execute('SELECT * FROM execute_steps WHERE execute_type_id=%s ORDER BY id;', (msg['execute_type_id'],))
        msg['execute_steps'] = [dict(x) for x in cur]
        cur.execute('SELECT id, time_limit, memory_limit, score FROM testdata WHERE problem_id=%s;', (msg['problem_id'],))
        msg['testdata'] = [dict(x) for x in cur]
        return res
    
    def send(self, sock, msg):
        try: sock.send((json.dumps(msg, cls=DatetimeEncoder)+'\r\n').encode())
        except socket.error: self.close_socket(sock)
        except Exception as e: print(e, 'send msg error')

    def get_submission(self):
        cur = self.cursor()
        delete_cur = self.cursor()
        cur.execute("SELECT * FROM wait_submissions")
        for x in cur:
            self.submission_queue.append(x['submission_id'])
            #delete_cur.execute("DELETE FROM wait_submissions WHERE id=%s", (x['id'],))

    def CommandHandler(self, cmd):
        print(cmd)
        if cmd.lower() == "exit":
            while len(self.client_pool):
                self.close_socket(self.client_pool[0])
            sys.exit()
        elif cmd.lower() == "insert":
            self.insert_submission()
        elif cmd.lower() == "restart":
            os.execv("/usr/bin/python3", ("python3", __file__,))
        else:
            print("Unkown commnad: ", cmd)

    def close_socket(self, sock):
        sock.close()
        self.client_pool.remove(sock)
        self.pool.remove(sock)

    def sock_auth_token(self, sock, token):
        cur = self.cursor()
        cur.execute('SELECT * FROM judge_token WHERE token=%s;', (token,))
        if cur.rowcount == 1:
            self.client[sock].type = map_sock_type['undefined']
            print('Client from addr: %s passed auth'%(self.client[sock].addr,))
            return True
        else:
            print('Client from addr: %s failed auth'%(self.client[sock].addr,))
            return False

    def sock_set_type(self, sock, type):
        if type in map_sock_type.values():
            self.client[sock].type = type
            return True
        else:
            return False

    def sock_send_type(self, sock):
        self.send(sock, {'cmd': 'type', 'msg': self.client[sock].type})

    def sock_update_submission(self, sock, msg):
        if not self.check_submission_meta(msg):
            return
        cur = self.cursor()
        cur.execute('DELETE FROM wait_submissions WHERE submission_id=%s;', (msg['submission_id'],))
        msg['score'] = sum(int(x['score']) if int(x['verdict'])==7 else 0 for x in msg['testdata'])
        msg['memory_usage'] = sum(int(x['memory_usage']) for x in msg['testdata'])
        msg['time_usage'] = sum(int(x['time_usage']) for x in msg['testdata'])
        msg['verdict'] = min(int(x['verdict']) for x in msg['testdata'])
        for testdata in msg['testdata']:
            cur.execute('UPDATE map_submission_testdata SET memory_usage=%s, time_usage=%s, verdict=%s WHERE submission_id=%s AND testdata_id=%s;', (testdata['memory_usage'], testdata['time_usage'], testdata['verdict'], msg['submission_id'], testdata['id'],))
        cur.execute('UPDATE submissions SET memory_usage=%s, time_usage=%s, score=%s, verdict=%s WHERE id=%s;', (msg['memory_usage'], msg['time_usage'], msg['score'], msg['verdict'], msg['submission_id'],))
        self.rs.delete('submission@%s'%(str(msg['submission_id'])))

    def sock_update_submission_testdata(self, sock, msg):
        pass

    def sock_send_submission(self, sock, submission_id):
        msg = self.gen_submission_meta(submission_id)
        self.send(sock, msg)

    def ReadSockHandler(self, sock):
        client = self.client[sock]
        msg = self.receive(sock)
        print('READ: ', msg, client.type)
        if msg is None: return
        if msg['cmd'] == 'type' and msg['msg'] == '':
            self.sock_send_type(sock)
        elif client.type == map_sock_type['unauth']:
            if msg['cmd'] == 'token':
                res = self.sock_auth_token(sock, msg['msg'])
                self.sock_send_type(sock)
            else:
                print('not auth')
        elif client.type == map_sock_type['undefined']:     # undefined
            if msg['cmd'] == 'type':
                self.sock_set_type(sock, msg['msg'])
                self.sock_send_type(sock)
            else:
                print('undefined')
        elif client.type == map_sock_type['judge']:   # judge
            if msg['cmd'] == 'judged':
                self.sock_update_submission(sock, msg['msg'])
                client.lock = 0
            elif msg['cmd'] == 'judged_testdata':
                pass
            else:
                print('unkown cmd')
        elif client.type == map_sock_type['web']:   # web
            pass
        else:
            print("error")
            self.close_socket(sock)

    def WriteSockHandler(self, sock):
        if sock not in self.client: return
        client = self.client[sock]
        if client.type == map_sock_type['unauth']:
            pass
        elif client.type == map_sock_type['undefined']:
            pass
        elif client.type == map_sock_type['judge']:
            if len(self.submission_queue) and client.lock == 0:
                self.sock_send_submission(sock, self.submission_queue.pop(0))
                client.lock = 1
        elif client.type == map_sock_type['web']:
            pass
        else:
            print('error')
            self.close_socket(sock)
    def insert_submission(self):
        cur = self.cursor()
        cur.execute("INSERT INTO wait_submissions (submission_id) VALUES (10002);")
        
    def run(self):
        while True:
            if len(self.submission_queue) == 0:
                self.get_submission()
            read_sockets, write_sockets, error_sockets = select.select(self.pool, [], [])
            for sock in read_sockets:
                if sock == self.s:
                    sockfd, addr = sock.accept()
                    self.pool.append(sockfd)
                    self.client_pool.append(sockfd)
                    self.client[sockfd] = self.CLIENT(addr)
                    print("client (%s, %s) connected" % addr)
                elif sock == sys.stdin:
                    self.CommandHandler(input())
                else:
                    self.ReadSockHandler(sock)
            for sock in self.client_pool:
                self.WriteSockHandler(sock)

if __name__ == "__main__":
    judgecenter = JudgeCenter()
    #judgecenter.insert_submission()
    judgecenter.run()
