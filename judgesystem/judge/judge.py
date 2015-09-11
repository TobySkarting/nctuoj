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
        self.s.setblocking(0)
        self.pool = [sys.stdin, self.s]
        self.recv_buffer_len = 1024
        #self.s.send(test.pop(0))
        #print(self.s.recv(1024))
        #self.s.send(test.pop(0))
        #print(self.s.recv(1024))

    def receive(self, sock):
        try:
            data = sock.recv(self.recv_buffer_len).decode()
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
            print(msg['msg'])
            time.sleep(2)
            for testdata in msg['msg']['testdata']:
                testdata['verdict'] = 0
            sock.send((json.dumps({"cmd":"judged", "msg":msg['msg']})+'\r\n').encode())
        else:
            print(msg)

    def send(self, sock, msg):
        try: sock.send((json.dumps(msg)+'\r\n').encode())
        except socket.error: self.close_socket(sock)
        except Exception as e: print(e, 'send msg error')

    def send_token(self):
        self.send(self.s, {'cmd': 'token', 'msg': 'TOKEN'})

    def send_type(self, type):
        self.send(self.s, {'cmd': 'type', 'msg': type})

    def CommandHandler(self, cmd):
        cmd = cmd.split()
        if cmd[0] == 'token':
            self.send_token()
        elif cmd[0] == 'type':
            self.send_type(int(cmd[1]))

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.pool, [self.s,], [], 0)
            for sock in read_sockets:
                if sock == sys.stdin:
                    self.CommandHandler(input())
                else:
                    self.SockHandler(sock)


if __name__ == "__main__":
    judge = Judge()
    judge.run()
