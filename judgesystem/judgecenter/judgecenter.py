### http://www.binarytides.com/python-socket-server-code-example/
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

        self.client = {}

    class CLIENT():
        def __init__(self):
            self.type = 0


    def run(self):
        while(1):
            read_sockets,write_sockets,error_sockets = select.select(self.pool,[],[])
            for sock in read_sockets:
                if sock == self.s:
                    sockfd, addr = sock.accept()
                    self.pool.append(sockfd)
                    self.client[sockfd] = CLIENT()
                    print("client (%s, %s) connected" % addr)
                else:
                    pass

if __name__ == "__main__":
    judgecenter = Judgecenter()
    judgecenter.run()
