### http://www.binarytides.com/python-socket-server-code-example/
import socket
import select
import config
import psycopg2
import psycopg2.extras
import ftp
import sys
import json
from map import *

SOCK_AVAILABLE_CMD = ['token', 'type', 'judged']

class JudgeCenter:
    def __init__(self):
        self.db = psycopg2.connect( host=config.db_host, dbname=config.db_dbname, user=config.db_user, password=config.db_password) 
        self.db.autocommit = True
        # self.ftp = ftp.FTP(config.ftp_server, config.ftp_port, config.ftp_user, config.ftp_password)

        self.recv_buffer_len = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((config.judgecenter_host, config.judgecenter_port))
        self.s.listen(config.judgecenter_listen)
        self.pool = [sys.stdin, self.s]
        self.client_pool = []
        self.recv_buffer_len = 1024
        self.submission_queue = [1,2,3,4]

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
        if 'submission_id' not in msg or 'testdatas' not in msg:
            return False
        for testdata in msg['testdatas']:
            if 'id' not in testdata or 'time' not in testdata or 'memory' not in testdata or 'verdict' not in testdata:
                return False
            try:
                testdata['id'] = int(testdata['id'])
                testdata['time'] = int(testdata['time'])
                testdata['memory'] = int(testdata['memory'])
                testdata['verdict'] = int(testdata['verdict'])
            except:
                return False
        return True
    
    def send(self, sock, msg):
        try: sock.send((json.dumps(msg)+'\r\n').encode())
        except socket.error: self.close_socket(sock)
        except: print('send msg error')

    def get_submission(self):
        cur = self.cursor()
        delete_cur = self.cursor()
        cur.execute("SELECT * FROM wait_submissions")
        for x in cur:
            self.submission_queue.append(x['submission_id'])
            delete_cur.execute("DELETE FROM wait_submissions WHERE id=%s", (x['id'],))

    def CommandHandler(self, cmd):
        print(cmd)

    def close_socket(self, sock):
        sock.close()
        self.client.pop(sock)
        self.pool.remove(sock)
        self.client_pool.remove(sock)

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
        pass

    def sock_send_submission(self, sock, submission_id):
        self.send(sock, {'cmd': 'judge', 'msg': {'submission_id': submission_id}})

    def ReadSockHandler(self, sock):
        client = self.client[sock]
        msg = self.receive(sock)
        print(msg)
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

    def run(self):
        while True:
            if len(self.submission_queue) == 0:
                self.get_submission()
            read_sockets, write_sockets, error_sockets = select.select(self.pool, self.client_pool, [])
            print(write_sockets)
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
            for sock in write_sockets:
                self.WriteSockHandler(sock)

if __name__ == "__main__":
    judgecenter = JudgeCenter()
    judgecenter.run()
