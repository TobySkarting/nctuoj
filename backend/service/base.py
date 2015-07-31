class BaseService:
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs

    def check_required_args(self, args, data):
        for a in args:
            if a not in data:
                return 'Error: %s should exist' % a
            if not data[a]:
                return 'Error: %s should not be empty.' % a
        return None

    def gen_insert_sql(self, tablename, data):
        '''
        tablename(str)
        data(dict)
        return sql(str), prama(tuple)
        '''
        sql1, sql2, prama = '', '', []
        for col in data:
            sql1 += ' `%s`,'%col
            sql2 += ' %s,'
            prama.append(data[col])
        ### remove last comma
        sql1, sql2 = sql1[:-1], sql2[:-1]
        sql = ('INSERT INTO `%s` '%tablename) + ('(%s) '%sql1) + ('VALUES(%s) '%sql2) + ''
        return (sql, tuple(prama))
    
    def gen_update_sql(self, tablename, data):
        '''
        tablename(str)
        data(dict)
        return sql(str), prama(tuple)
        '''
        sql, prama = '', []
        for col in data:
            sql += ((' `%s` = '%col) + '%s,')
            prama.append(data[col])
        ### remove last comma
        sql = sql[:-1]
        sql = 'UPDATE `%s` SET %s '%(tablename, sql)
        return (sql, tuple(prama))

    def gen_select_sql(self, tablename, data):
        '''
        tablename(str)
        data(list)
        return sql(str)
        '''
        sql = ''
        for col in data:
            sql += ' `%s`,'%col
        ### remove last comma
        sql = sql[:-1]
        sql = 'SELECT %s FROM %s '%(sql, tablename)
        return sql
