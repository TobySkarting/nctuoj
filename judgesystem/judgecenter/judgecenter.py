import socket
import config
import psycopg2


class Judgecenter:
    def __init__(self):
        self.db = psycopg2.connect( host=config.db_host, dbname=config.db_dbname, user=config.db_user, password=config.db_password) 

    def run(self):
        while(1):
            pass

if __name__ == "__main__":
    judgecenter = Judgecenter()
    judgecenter.run()
