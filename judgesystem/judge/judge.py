import socket
import select
import config
import psycopg2
import ftp

class Judge:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((config.judgecenter_host, config.judgecenter_port))
        pass

if __name__ == "__main__":
    judge = Judge()
