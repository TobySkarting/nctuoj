import paramiko, sys
from scp import SCPClient
import os
import datetime
import sys
import config


class FTP:
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password

    def createSSHClient(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.server, self.port, self.user, self.password)
        return client
    
    def get(self, _from, _to):
        ssh = self.createSSHClient()
        scp = SCPClient(ssh.get_transport())
        try: os.makedirs(os.path.split(_to)[0])
        except: pass
        scp.get(_from, _to)
        scp.close()

    def put(self, _from, _to):
        ssh = self.createSSHClient()
        try: ssh.exec_command('mkdir -p ' + os.path.split(_to)[0])
        except: pass
        scp = SCPClient(ssh.get_transport())
        scp.put(_from, _to)
        scp.close()

    def delete(self, _target):
        ssh = self.createSSHClient()
        try: ssh.exec_command('rm -rf ' + _target)
        except: pass

if __name__ == "__main__":
    ftp = FTP(config.FTPSERVER, config.FTPPORT, config.FTPUSER, config.FTPPASSWD)
    action = sys.argv[1]
    if action.lower() == "upload":
        ftp.put(sys.argv[2], sys.argv[3])
