import socket
import os
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
import errno
import time
from isolate import Sandbox
import subprocess as sp

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
        times = 0
        delay = [5, 10, 30, 60, 300]
        while True:
            try:
                self.s.connect((config.judgecenter_host, config.judgecenter_port))
                break
            except:
                print("Cannot connect to judgecenter. Retry after %s second." % delay[times])
                time.sleep(delay[times])
                times = min(times+1, 4)

        #self.s.setblocking(0)
        self.pool = [sys.stdin, self.s]
        self.recv_buffer_len = 1024

    def receive(self):
        sock = self.s
        data = ""
        sock.setblocking(0)
        while True:
            try:
                tmp = sock.recv(self.recv_buffer_len)
            except Exception as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    break
                else:
                    return []
            else:
                data += tmp.decode()
                if len(data)==0:
                    self.restart()


        data = data.split("\r\n")
        res = []
        for x in data:
            if len(x):
                try:
                    res.append(json.loads(x))
                except:
                    print("err: %s" % x)
        return res

    def get_testdata(self,testdata):
        for x in testdata:
            remote_path = './data/testdata/%s/'%(str(x['id']))
            file_path = '%s/testdata/'%(config.store_folder)
            try: shutil.rmtree(file_path)
            except: pass
            self.ftp.get(remote_path, file_path)

    def get_submission(self, submission_id):
        remote_path = './data/submissions/%s/'%(str(submission_id))
        file_path = '%s/submissions/%s/'%(config.store_folder,str(submission_id))
        try: shutil.rmtree(file_path)
        except: pass
        self.ftp.get(remote_path, file_path)


    def judge(self, msg):
        print(msg)
        self.get_testdata(msg['testdata'])
        self.get_submission(msg['submission_id'])
        s = Sandbox(os.getpid(), './isolate')
        s.set_options(proc_limit=4, meta='meta', errput='err', mem_limit=65535*20)
        s.init_box()
        ### move submission file to isolate
        submission_file = "%s/submissions/%s/%s"%(config.store_folder, msg['submission_id'], msg['file_name'])
        sandbox_file = "/tmp/box/%s/box/"%(os.getpid())
        print(submission_file)
        sp.call("cat %s"%(submission_file), shell=True)
        sp.call("cp %s %s"%(submission_file, sandbox_file), shell=True)
        s.exec_box("/usr/bin/env ls")
        ### All of thing except last


        ### for the last
        for testdata in msg['testdata']:
            testdata['verdict'] = 7
            testdata['time_usage'] = testdata['time_limit']/2
            testdata['memory_usage'] = testdata['memory_limit']/2
            self.send({"cmd":"judged_testdata", "msg":msg})
        self.send({"cmd":"judged", "msg":msg})
        s.delete_box()

    def SockHandler(self):
        MSGS = self.receive()
        for msg in MSGS:
            if len(msg)==0: continue
            if msg['cmd'] == 'judge':
                self.judge(msg['msg'])
            else:
                print(msg)

    def restart(self):
        os.execv("/usr/bin/python3", ("python3", __file__,))

    def send(self, msg):
        try: self.s.sendall((json.dumps(msg, cls=DatetimeEncoder)+'\r\n').encode())
        except socket.error: self.close_socket(self.s)
        except Exception as e: print(e, 'send msg error')

    def send_token(self):
        print("send token")
        self.send({'cmd': 'token', 'msg': 'TOKEN'})
        
    def send_type(self, type):
        print("send type")
        self.send({'cmd': 'type', 'msg': type})

    def CommandHandler(self):
        cmd = input()
        param = cmd.lower().split(' ')
        cmd = param[0]
        if cmd == "restart":
            self.restart()
        elif cmd.lower() == 'exit':
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
    print("====start====")
    if(os.getuid() != 0):
        print("This program need root! Do you want to run it as root?(Y/N)")
        x = input().lower()
        if x == "y":
            os.execv("/usr/bin/sudo", ("sudo", "python3", __file__,))
        else:
            sys.exit(0)
    print(os.getcwd())
    judge = Judge()
    judge.send_token()
    judge.send_type(1)
    judge.run()
