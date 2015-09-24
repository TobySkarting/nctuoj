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
import re
#from backend
map_lang = {
    0:  "C",
    1:  "C++",
    2:  "Java",
    3:  "Python2",
    4:  "Python3",
    5:  "Go",
    6:  "Perl",
    7:  "Javascript",
    8:  "Haskell",
    9:  "ruby",
    10: "sh",
}

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
        try: os.makedirs('%s/submissions/'%(config.store_folder))
        except: pass
        try: os.makedirs('%s/testdata/lock/'%(config.store_folder))
        except: pass
        try: os.makedirs('%s/testdata/config/'%(config.store_folder))
        except: pass
        try: os.makedirs('%s/verdict/lock/'%(config.store_folder))
        except: pass
        try: os.makedirs('%s/verdict/config/'%(config.store_folder))
        except: pass

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

    
    def lock_get(self, _from, _to, _config, _lock, timestamp):
        def read_config(path, timestamp):
            try:
                f = open(path)
                t = f.read()
                return t == str(timestamp)
            except:
                return False
        def write_config(path, timestamp):
            f = open(path, "w+")
            f.write(str(timestamp))
            f.close()
        while True:
            if read_config(_config, timestamp):
                break
            if os.path.exists(_lock):
                time.sleep(0.01)
            else:
                f = open(_lock, "w+")
                f.close()
                print("download: ", _from, _to)
                self.ftp.get(_from, _to)
                write_config(_config, timestamp)
                os.remove(_lock)

    def get_testdata(self,testdata):
        for x in testdata:
            remote_path = './data/testdata/%s/'%(str(x['id']))
            file_path = '%s/testdata/'%(config.store_folder)
            lock_path = '%s/testdata/lock/%s'%(config.store_folder, x['id'])
            config_path = '%s/testdata/config/%s'%(config.store_folder, x['id'])
            self.lock_get(remote_path, file_path, config_path, lock_path, x['updated_at'])

    def get_submission(self, submission_id):
        remote_path = './data/submissions/%s/'%(str(submission_id))
        file_path = '%s/submissions/'%(config.store_folder)
        try: shutil.rmtree("%s/%s"%(file_path,str(submission_id)))
        except: pass
        self.ftp.get(remote_path, file_path)


    def read_meta(self, file_path):
        res = {
            "status": "AC",
            "time": 0,
            "memory": 0,
            "exitcode": 0,
        }
        f = open(file_path).readlines()
        for x in f:
            x = x.strip('\n').split(":")
            if x[0] == "status":
                res['status'] = x[1]
            elif x[0] == "time":
                res["time"] = int(1000*float(x[1]))
            elif x[0] == "max-rss":
                res["memory"] = int(x[1])
            elif x[0] == "exitcode":
                res['exitcode'] = int(x[1])
            else:
                res[x[0]] = x[1]
        if res['status'] == "TO":
            res['status'] = "TLE"
        if res['status'] == "SG":
            res['status'] = "RE" 
        print(res)
        return res


    def compile(self, msg):
        sandbox = Sandbox(os.getpid(), './isolate')
        sandbox.folder = "/tmp/box/%s/box/"%(os.getpid())
        print("Box: ", sandbox.folder)
        sandbox.options = {
            "proc_limit": 4,
            "meta": "%s/meta"%(sandbox.folder),
            #"output": "output",
            #"errput": "errput",
            "mem_limit": 262144,
            "time_limit": 3,
        }
        ### special option for each lang

        if map_lang[msg['execute_type']['lang']] == "Java":
            sandbox.options['mem_limit'] = 0
            sandbox.options['proc_limit'] = 16
        sandbox.init_box()
        sandbox.set_options(**sandbox.options)
        sp.call("cp %s/submissions/%s/%s %s"%(config.store_folder, msg['submission_id'], msg['file_name'], sandbox.folder), shell=True)
        res = {
            "status": "AC",
            "exitcode": 0,
        }
        for step in range(len(msg['execute_steps']) - 1):
            run_cmd = msg['execute_steps'][step]['command']
            run_cmd = self.cmd_replace(run_cmd, {
                "file_name": msg['file_name'],
                "memory_limit": 262144,
                })
            sandbox.exec_box("/usr/bin/env %s" % run_cmd)
            res = self.read_meta(sandbox.options['meta'])
            if res['exitcode'] != 0:
                return (res, sandbox)
        return (res, sandbox)

    def send_judged_testdata(self, res, testdata, msg):
        self.send({
            'cmd': 'judged_testdata',
            'msg': {
                'submission_id': msg['submission_id'],
                'testdata_id': testdata['id'],
                'status': res['status'],
                'verdict': self.map_verdict_string[res['status']],
                'time_usage': res['time'],
                'memory_usage': res['memory'],
                'score': int(res['score'] * int(testdata['score']))
            }
        })

    def verdict(self, file_a, file_b):
        a = open(file_a, "r").readlines()
        b = open(file_b, "r").readlines()
        verdict = "WA" if a != b else "AC"
        score = 1.0 if a == b else 0.0
        return (verdict, score)

    def cmd_replace(self, cmd, param):
        if "file_name" in param:
            cmd = cmd.replace("__FILE__", param['file_name'])
            cmd = cmd.replace("__FILE_EXTENSION__", param['file_name'].split(".")[-1])
            cmd = cmd.replace("__MAIN_FILE__", ('.').join(param['file_name'].split(".")[:-1]))
        if "memory_limit" in param:
            cmd = cmd.replace("__MEMORY_LIMIT__", str(param['memory_limit']))
        return cmd

    def exec(self, sandbox, testdata, msg):
        run_cmd = msg['execute_steps'][-1]['command']
        run_cmd = self.cmd_replace(run_cmd, {
            "file_name": msg['file_name'],
            "memory_limit": testdata['memory_limit'],
            })
        sp.call("cp %s/testdata/%s/input %s"%(config.store_folder, testdata['id'], sandbox.folder), shell=True)
        sandbox.options['input'] = "input"
        sandbox.options['time_limit'] = testdata['time_limit'] / 1000
        sandbox.options['mem_limit'] = testdata['memory_limit']
        sandbox.options['fsize_limit'] = 65536
        sandbox.options['output'] = "output"
        sandbox.options["errput"] = "errput"
        ### special option for each lang
        if map_lang[msg['execute_type']['lang']] == "Java":
            sandbox.options['mem_limit'] = 0
            sandbox.options['proc_limit'] = 16

        sandbox.set_options(**sandbox.options)
        sandbox.exec_box("/usr/bin/env %s" % run_cmd)
        res = self.read_meta(sandbox.options['meta'])
        if res['memory'] > testdata['memory_limit']:
            res['status'] == "MLE"
        res['score'] = 0
        if res['status'] == "AC":
            res['status'], res['score'] = self.verdict("%s/testdata/%s/output"%(config.store_folder, testdata['id']), "%s/output"%(sandbox.folder))
        self.send_judged_testdata(res, testdata, msg)
        return res


    def judge(self, msg):
        print(msg)
        self.get_testdata(msg['testdata'])
        self.get_submission(msg['submission_id'])

        if msg['execute_type']['recompile'] == 0:
            print("Don't compile everytime!")
            res, sandbox = self.compile(msg)
            if res['status'] != "AC":
                for testdata in msg['testdata']:
                    self.send({
                        'cmd': 'judged_testdata',
                        'msg': {
                            'submission_id': msg['submission_id'],
                            'testdata_id': testdata['id'],
                            'status': 'CE',
                            'verdict': self.map_verdict_string['CE']
                        }
                    })
                self.send({"cmd":"judged", "msg":""})
                sandbox.delete_box()
                return
            for testdata in msg['testdata']:
                res = self.exec(sandbox, testdata, msg)
            sandbox.delete_box()
        else:
            for testdata in msg['testdata']:
                res, sandbox = self.compile(msg)
                self.exec(sandbox, testdata, msg)
                sandbox.delete_box()
                    
        self.send({"cmd":"judged", "msg":""})

    def SockHandler(self):
        MSGS = self.receive()
        for msg in MSGS:
            if len(msg)==0: continue
            if msg['cmd'] == 'judge':
                self.judge(msg['msg'])
            elif msg['cmd'] == 'map_verdict_string':
                self.map_verdict_string = {}
                for x in msg['msg']:
                    self.map_verdict_string[x['abbreviation']] = int(x['id'])
                print(self.map_verdict_string)
            elif msg['cmd'] == 'restart':
                self.restart()
            else:
                print(msg)

    def restart(self):
        os.execv("/usr/bin/python3", ("python3", __file__,))

    def send(self, msg):
        try: self.s.sendall((json.dumps(msg, cls=DatetimeEncoder)+'\r\n').encode())
        except socket.error: self.restart()
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
    judge = Judge()
    judge.send_token()
    judge.send_type(1)
    judge.run()
