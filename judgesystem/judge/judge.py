import socket
import select
import config
import psycopg2
from ftp import FTP
import select
import json
import sys
import time
import shutil
import datetime

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class Judge:
    def __init__(self):
        self.ftp = FTP(config.ftp_server, config.ftp_port, config.ftp_user, config.ftp_password)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((config.judgecenter_host, config.judgecenter_port))
        self.s.setblocking(0)
        self.pool = [sys.stdin, self.s]
        self.recv_buffer_len = 1024

    def receive(self):
        sock = self.s
        try:
            data = sock.recv(self.recv_buffer_len).decode()
            if data == '':
                raise socket.error
            res = json.loads(data)
        except socket.error:
            res = None
            self.s.close()
            sys.exit(1)
        except Exception as e:
            res = None
            print(e, 'receive msg error')
        if res and ('cmd' not in res or 'msg' not in res):
            res = None
        return res

    def get_testdata(self,testdata):
        for x in testdata:
            remote_path = './data/testdata/%s/'%(str(x['id']))
            file_path = '../../data/testdata/%s/'%(str(x['id']))
            try: shutil.rmtree(file_path)
            except: pass
            self.ftp.get(remote_path, file_path)

    def get_submission(self, submission_id):
        remote_path = './data/submissions/%s/'%(str(submission_id))
        file_path = '../../data/submissions/%s/'%(str(submission_id))
        try: shutil.rmtree(file_path)
        except: pass
        self.ftp.get(remote_path, file_path)


    def judge(self, msg):
        self.get_testdata(msg['testdata'])
        self.get_submission(msg['submission_id'])
        for testdata in msg['testdata']:
            testdata['verdict'] = 7
            testdata['time_usage'] = testdata['time_limit']/2
            testdata['memory_usage'] = testdata['memory_limit']/2
        return msg

    def SockHandler(self):
        msg = self.receive()
        if msg is None: return
        if msg['cmd'] == 'judge':
            print(msg['msg'])
            time.sleep(1)
            msg = self.judge(msg['msg'])
            self.send({"cmd":"judged", "msg":msg})
        else:
            print(msg)

    def send(self, msg):
        try: self.s.send((json.dumps(msg, cls=DatetimeEncoder)+'\r\n').encode())
        except socket.error: self.close_socket(self.s)
        except Exception as e: print(e, 'send msg error')

    def send_token(self):
        self.send({'cmd': 'token', 'msg': 'TOKEN'})

    def send_type(self, type):
        self.send({'cmd': 'type', 'msg': type})

    def CommandHandler(self):
        cmd = input()
        cmd = cmd.split()
        if cmd[0] == 'token':
            self.send_token()
        elif cmd[0] == 'type':
            self.send_type(int(cmd[1]))
        elif cmd[0].lower() == 'exit':
            sys.exit(0)

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.pool, [], [])
            for sock in read_sockets:
                if sock == sys.stdin:
                    self.CommandHandler()
                else:
                    self.SockHandler()


if __name__ == "__main__":
    judge = Judge()
    judge.run()
