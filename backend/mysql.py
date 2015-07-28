import tormysql
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
                charset = self._charset
                )

    def get_conn(self):
        conn = yield self._pool.Connection()
        return conn

    def execute(self, sql, prama=(), col=()):
        conn = yield from self.get_conn()
        cur = conn.cursor()
        yield cur.execute(sql, prama)
        if len(col):
            _x = list(cur.fetchall())
            res = []
            for _ in _x:
                res.append(dict(zip(col, _)))
        else:
            res = cur.fetchall()
        yield cur.close()
        conn.close()
        return res

    def flush_tables(self):
        yield from self.execute('FLUSH TABLES;')
