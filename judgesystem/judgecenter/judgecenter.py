import socket
import config
import psycopg2
import ftp


class Judgecenter:
    def __init__(self):
        self.db = psycopg2.connect( host=config.db_host, dbname=config.db_dbname, user=config.db_user, password=config.db_password) 
        self.ftp = ftp.FTP(config.ftp_server, config.ftp_port, config.ftp_user, config.ftp_password)



        self.recv_buffer_len = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind('localhost', config.judgecenter_port)
        self.s.listen(config.judgecenter_listen)
        self.pool = [sys.stdin, self.s]   


    def run(self):
        while(1):
            pass

if __name__ == "__main__":
    judgecenter = Judgecenter()
    judgecenter.run()
