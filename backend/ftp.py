import paramiko, sys
import time
from scp import SCPClient
import os
import datetime
import sys
import config
import tornado
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class FTP:
    executor = ThreadPoolExecutor(config.FTP_THREADPOOL_SIZE)
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.createSSHClient()
    
    def createSSHClient(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.server, self.port, self.user, self.password)
    
    @run_on_executor
    def get(self, _from, _to):
        scp = SCPClient(self.client.get_transport())
        try: os.makedirs(os.path.split(_to)[0])
        except: pass
        scp.get(_from, _to)
        scp.close()

    @run_on_executor
    def put(self, _from, _to):
        try: self.client.exec_command('mkdir -p %s' % os.path.split(_to)[0])
        except Exception as e: print(e)
        scp = SCPClient(self.client.get_transport())
        scp.put(_from, _to)
        scp.close()

    @run_on_executor
    def delete(self, _target):
        try: self.client.exec_command('rm -rf %s' % _target)
        except: pass

