import paramiko, sys
import time
from scp import SCPClient
import os
import datetime
import sys
import config

def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

class FTP:
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
    
    def get(self, _from, _to):
        scp = SCPClient(self.client.get_transport())
        try: os.makedirs(os.path.split(_to)[0])
        except: pass
        scp.get(_from, _to)
        scp.close()

    def put(self, _from, _to):
        try: self.client.exec_command('mkdir -p %s' % os.path.split(_to)[0])
        except Exception as e: print(e)
        scp = SCPClient(self.client.get_transport())
        scp.put(_from, _to)
        scp.close()

    def delete(self, _target):
        try: self.client.exec_command('rm -rf %s' % _target)
        except: pass

    def upload(self, local, remote):
        self.put(local, remote)
    def download(self, remote, local):
        self.get(remote, local)

    """
    def upload(self, local, remote):
        p = multiprocessing.Process(target=self.put, args=(local, remote,))
        p.start()
        while p.exitcode == None:
            yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 0.01)

    def download(self, remote, local):
        p = multiprocessing.Process(target=self.put, args=(get, remote,))
        p.start()
        while p.exitcode == None:
            yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 0.01)
    """

if __name__ == "__main__":
    """
    ftp = FTP(config.FTPSERVER, config.FTPPORT, config.FTPUSER, config.FTPPASSWD)
    action = sys.argv[1]
    if action.lower() == "upload":
        ftp.put(sys.argv[2], sys.argv[3])
    elif action.lower() == "download":
        ftp.get(sys.argv[2], sys.argv[3])
    """
    pass
