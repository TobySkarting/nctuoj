import paramiko, sys
from scp import SCPClient
import os
import time
import datetime
import sys

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
        while True:
            try:
                scp = SCPClient(self.client.get_transport())
                try: os.makedirs(os.path.split(_to)[0])
                except: pass
                scp.get(_from, _to, recursive=True)
                scp.close()
                return
            except:
                pass

    def put(self, _from, _to):
        try: ssh.exec_command('mkdir -p %s' % os.path.split(_to)[0])
        except: pass
        scp = SCPClient(self.client.get_transport())
        scp.put(_from, _to)
        scp.close()

    def delete(self, _target):
        try: self.client.exec_command('rm -rf %s' % _target)
        except: pass

if __name__ == "__main__":
    ftp = FTP("localhost", 22, "nctuojftp", "nctuojftp")
    print("sleep")
    time.sleep(100)
    ftp.put("./meta", "./")



    pass
