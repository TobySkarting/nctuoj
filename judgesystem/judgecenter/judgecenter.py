### http://www.binarytides.com/python-socket-server-code-example/
import socket
import select
import config
import psycopg2
import psycopg2.extras
import ftp
import sys


class JudgeCenter:
    def __init__(self):
        self.db = psycopg2.connect( host=config.db_host, dbname=config.db_dbname, user=config.db_user, password=config.db_password) 
        self.db.autocommit = True
        # self.ftp = ftp.FTP(config.ftp_server, config.ftp_port, config.ftp_user, config.ftp_password)

        self.recv_buffer_len = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((config.judgecenter_host, config.judgecenter_port))
        self.s.listen(config.judgecenter_listen)
        self.pool = [sys.stdin, self.s]   

        self.submission_queue = []

        self.client = {}

    class CLIENT():
        def __init__(self):
            self.type = 0
            client.close()
            self.client.pop(sock)
        

    def get_submission(self):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        delete_cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM wait_submissions")
        for x in cur:
            self.submission_queue.append(x['submission_id'])
            delete_cur.execute("DELETE FROM wait_submissions WHERE id=%s", (x['id'],))
        print(self.submission_queue)

    def CommandHandler(self, cmd):
        print(cmd)
        pass

    def close_socket(self, sock):
        self.client[sock].close()
        self.client.pop(sock)

    def SockHandler(self, sock):
        client = self.client[sock]
        if client.type == 0:     # undefined
            
            pass
        elif client.type == 1:   # judge
            pass
        elif client.type == 2:   # web
            pass
        else:
            print("error")
            self.close_socket(sock)

    def run(self):
        while(1):
            if len(self.submission_queue) == 0:
                self.get_submission()
            read_sockets, write_sockets, error_sockets = select.select(self.pool, [], [])
            for sock in read_sockets:
                if sock == self.s:
                    sockfd, addr = sock.accept()
                    self.pool.append(sockfd)
                    self.client[sockfd] = self.CLIENT()
                    print("client (%s, %s) connected" % addr)
                elif sock == sys.stdin:
                    self.CommandHandler(input())
                else:
                    self.SockHandler(sock)

if __name__ == "__main__":
    judgecenter = JudgeCenter()
    judgecenter.get_submission()
    judgecenter.get_submission()
