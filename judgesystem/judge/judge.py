import socket
import select
import config
import psycopg2
import ftp
import select
import json
import sys
import time


test = [(json.dumps({'cmd': 'token', 'msg': 'TOKEN'})+'\r\n').encode(),(json.dumps({'cmd': 'type', 'msg': 1})+'\r\n').encode()]

class Judge:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((config.judgecenter_host, config.judgecenter_port))
        self.pool = [sys.stdin, self.s]
        self.recv_buffer_len = 1024
        self.s.send(test.pop(0))
        print(self.s.recv(1024))
        self.s.send(test.pop(0))
        print(self.s.recv(1024))

    def receive(self, sock):
        try:
            data = sock.recv(self.recv_buffer_len).decode()
            print('DATA: ', data)
            if data == '':
                raise socket.error
            res = json.loads(data)
        except socket.error:
            res = None
            #self.close_socket(sock)
        except Exception as e:
            res = None
            print(e, 'receive msg error')
        if res and ('cmd' not in res or 'msg' not in res):
            res = None
        return res

    def SockHandler(self, sock):
        msg = self.receive(sock)
        if msg is None: return
        if msg['cmd'] == 'judge':
            time.sleep(5)
            sock.send((json.dumps({"cmd":"judged", "msg":""})+'\r\n').encode())
        else:
            print(msg)


    def CommandHandler(self, cmd):
        print(cmd)

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.pool, [self.s,], [])
            for sock in read_sockets:
                if sock == sys.stdin:
                    self.CommandHandler(input())
                else:
                    self.SockHandler(sock)

            for sock in write_sockets:
                if len(test):
                    sock.send(test.pop(0))


        pass

if __name__ == "__main__":
    judge = Judge()
    judge.run()
