import paramiko, sys
from scp import SCPClient
import os
import datetime
import sys

class FTP:
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        createSSHClient()

    def createSSHClient(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.server, self.port, self.user, self.password)
    
    def get(self, _from, _to):
        scp = SCPClient(slef.client.get_transport())
        try: os.makedirs(os.path.split(_to)[0])
        except: pass
        scp.get(_from, _to)
        scp.close()

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
    pass
"""
    ftp = FTP(config.FTPSERVER, config.FTPPORT, config.FTPUSER, config.FTPPASSWD)
    action = sys.argv[1]
    if action.lower() == "upload":
        ftp.put(sys.argv[2], sys.argv[3])
    elif action.lower() == "download":
        ftp.get(sys.argv[2], sys.argv[3])
"""
