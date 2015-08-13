import tormysql
import sys
class AsyncMysql:
    def __init__(self, user, database, passwd, host='127.0.0.1', charset='utf8', **kwargs):
        self._user = user
        self._database = database
        self._passwd = passwd
        self._host = host
        self._charset = charset

        self._pool = tormysql.ConnectionPool(
                host = self._host,
                user = self._user,
                passwd = self._passwd,
                db = self._database,
                charset = self._charset,
                autocommit = True,
                )

    def get_conn(self):
        conn = yield self._pool.Connection()
        return conn

    def execute(self, sql, prama=()):
        conn = yield from self.get_conn()
        cur = conn.cursor(tormysql.cursor.DictCursor)
        try:
            yield cur.execute(sql, prama)
        except:
            print(str(sys.exc_info()[0]))
            yield cur.close()
            conn.close()
            return None
        res = cur.fetchall()
        yield cur.close()
        conn.close()
        if conn.insert_id():
            return conn.insert_id()
        else:
            return res
