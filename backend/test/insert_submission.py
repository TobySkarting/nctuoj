import mysql.connector
import random
class MySQL:
    def __init__(self, host='127.0.0.1', user="root", password="", database="", port=3306, charset='utf8'):
        self._config = {}
        self._config["host"] = host
        self._config["user"] = user
        self._config["password"] = password
        self._config["database"] = database
        self._config["port"] = port
        self._config["charset"] = charset
        """
        self._host = host
        self._user = user
        self._passwd = passwd
        self._database = database
        self._port = port
        """
    def connect(self):
        self.db = mysql.connector.connect(**self._config)

    def close(self):
        self.db.close()

    def execute(self, sql, parma = ()):
        self.connect()
        cursor = self.db.cursor()
        cursor.execute(sql, parma)
        meta = []
        for result in cursor.stored_results():
            meta = result.fetchall()
            print(meta)
        if sql.split()[0].lower() != "select":
            self.flush()
        else:
            meta = cursor.fetchall()
        self.close()
        return meta

    def flush(self):
        self.db.commit()

    def gen_insert_sql(self, tablename, data):
        sql1, sql2, prama = '', '', []
        for col in data:
            sql1 += ' `%s`,'%col
            sql2 += ' %s,'
            prama.append(data[col])
        sql1, sql2 = sql1[:-1], sql2[:-1]
        sql = ('INSERT INTO `%s` (%s) VALUES(%s)'%(tablename,sql1,sql2))
        return (sql, tuple(prama))

    def gen_update_sql(self, tablename, data):
        sql, prama = '', []
        for col in data:
            sql += ' `%s` = %%s,'%col
            prama.append(data[col])
        sql = sql[:-1]
        sql = 'UPDATE `%s` SET %s'%(tablename, sql)
        return (sql, tuple(prama))

    def gen_select_sql(self, tablename, data):
        sql = ''
        for col in data:
            sql += ' `%s`,'%col
        sql = sql[:-1]
        sql = 'SELECT %s FROM %s '%(sql, tablename)
        return sql

if __name__ == '__main__':
    db = MySQL('140.113.194.120', 'nctuoj', 'yavaf2droyPo', 'nctuoj')
    db.connect();
    for x in range(0, 10**6):
        sql = '''INSERT INTO `submissions` (`user_id`, `problem_id`, `execute_type_id`, `time_usage`, `memory_usage`, `score`) VALUES(%s, %s, %s, %s, %s, %s) '''
        db.execute(sql, (random.randint(1, 100), random.randint(1, 100), random.randint(1, 5), random.randint(1, 65535), random.randint(1, 65535), random.randint(1, 100)))
