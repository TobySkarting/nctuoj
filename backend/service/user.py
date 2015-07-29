from service.base import BaseService
import hashlib
import config

def _hash(pwd):
    hpwd = hashlib.sha512(str(pwd).encode()).hexdigest() + config.PASSWORD_KEY
    hpwd = hashlib.md5(str(pwd).encode()).hexdigest()
    return hpwd

class UserService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        UserService.inst = self

    def get_users_info(self, meta={}):
        col = ["id", "account", "email", "student_id", "school_id", "created_at"]
        sql = self.gen_select_sql("users", col)
        res = yield from self.db.execute(sql, (), col)
        for x in res:
            err, power = yield from self.get_user_power_info(x["id"])
            x["power"] = power
        yield from self.db.flush_tables()
        return (None, res)

    def get_user_basic_info(self, id):
        col = ["id", "account", "passwd", "email", "student_id", "school_id", "created_at", "updated_at"]
        res = yield from self.db.execute("SELECT * FROM users where id=%s", (id,), col)
        if len(res) == 0:
            return ('Eidnotexist', None)
        res = res[0]
        res.pop("passwd")
        yield from self.db.flush_tables()
        return (None, res)

    def get_user_group_info(self, id):
        col = ["id", "name", "description"]
        res = yield from self.db.execute("SELECT groups.id, groups.name, groups.description FROM groups inner join (select group_id from map_group_user where user_id = %s order by group_id) as b on groups.id = b.group_id", (id,), col)
        yield from self.db.flush_tables()
        return (None, res)

    def get_user_power_info(self, id):
        res = yield from self.db.execute("SELECT `right` from map_user_right WHERE user_id=%s", (id,))
        power = set()
        for x in res:
            power.add(x[0])
        yield from self.db.flush_tables()
        return (None, power)

    def get_user_group_power_info(self, uid, gid):
        res = yield from self.db.execute("SELECT `right` from map_group_user_right where user_id=%s AND group_id=%s", (uid, gid,))
        power = set()
        for x in res:
            power.add(x[0])
        yield from self.db.flush_tables()
        return (None, power)

    def modify(self, data={}):
        pass

    def SignIn(self, data, req): #need to set cookie
        '''
        data(dict): account(str), passwd(str)
        return id(str)
        '''
        ### check required arguemts
        required_args = ['account', 'passwd']
        if not self.check_required_args(required_args, data) :
            return ('Etoofewargs', None)
        ### check data validation
        err = self.check_data_not_empty(data)
        if err:
            return (err, None)
        ### get hashed passwd
        col = ['passwd', 'id']
        sql = self.gen_select_sql('users', col)
        res = yield from self.db.execute(sql+
                'WHERE `account` = %s;',
                (data['account'],), col)
        ### check account 
        if len(res) == 0:
            return ('Euser', None)
        hpwd, id = res[0]["passwd"], res[0]["id"]
        ### check passwd
        if _hash(data['passwd']) != hpwd:
            return ('Epasswd', None)
        req.set_secure_cookie('id', str(id))
        yield from self.db.flush_tables()
        return (None, str(id))

    def SignOut(self, req):
        req.clear_cookie('id')

    def SignUp(self, data={}):
        '''
        data(dict): account(str), student_id(str), passwd(str), repasswd(str), email(str), school_id
        return id(str)
        '''
        ### check required arguemts
        required_args = ['account', 'student_id', 'passwd', 'repasswd', 'email', 'school_id']
        if not self.check_required_args(required_args, data) :
            return ('Etoofewargs', None)
        ### check data valadation
        err = self.check_data_not_empty(data)
        if err:
            return (err, None)
        if data['passwd'] != data['repasswd']:
            return ('Econfirmpwd', None)

        ### check conflict
        res = yield from self.db.execute('SELECT `id` FROM `users` ' 
                'WHERE `account` = %s OR `student_id` = %s', 
                (data['account'], data['student_id'],))
        if len(res) != 0:
            return ('Eexist', None)

        ### gen hashed passwd
        hpasswd = _hash(data['passwd'])
        ### gen sql query
        data['passwd'] = hpasswd
        data.pop('repasswd')
        sql, prama = self.gen_insert_sql('users', data)
        res = yield from self.db.execute(sql, prama)
        res = yield from self.db.execute('SELECT `id` FROM `users` '
                'WHERE `account` = %s',
                (data['account'],), ["id",])
        if len(res) == 0:
            return ('Ecreate', None)
        id = res[0]["id"]
        yield from self.db.flush_tables()
        return (None, str(id))

