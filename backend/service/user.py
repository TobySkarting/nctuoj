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

    def get_user_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        res = yield from self.db.execute("SELECT * FROM users, (SELECT id FROM users ORDER BY id LIMIT %s, %s) AS b WHERE users.id = b.id", ((int(data['page'])-1)*int(data['count']), data['count'],))
        for x in res:
            err, x["power"] = yield from self.get_user_power_info(x["id"])
        return (None, res)

    def get_user_list_count(self, data={}):
        res = self.rs.get('user_list_count')
        if res: return (None, res)
        res = yield from self.db.execute("SELECT COUNT(*) FROM users")
        self.rs.set('user_list_count', res[0]['COUNT(*)'])
        return (None, res[0]['COUNT(*)'])

    def get_user_basic_info(self, id):
        res = self.rs.get("user_basic@%s" % str(id))
        if res: return (None, res)
        res = yield from self.db.execute("SELECT * FROM users where id=%s", (id,))
        if len(res) == 0:
            return ('Eidnotexist', None)
        res = res[0]
        res.pop("passwd")
        self.rs.set("user_basic@%s" % str(id), res)
        return (None, res)

    def get_user_group_info(self, id):
        res = self.rs.get('user_group@%s' % str(id))
        if res: return (None, res)
        res = yield from self.db.execute("SELECT groups.* FROM groups, (select group_id from map_group_user where user_id = %s order by group_id) as b WHERE groups.id = b.group_id", (id,))
        self.rs.set('user_group@%s' % str(id), res)
        return (None, res)

    def get_user_power_info(self, id):
        res = self.rs.get('user_power@%s' % str(id))
        if res: return (None, res)
        res = yield from self.db.execute("SELECT `power` from map_user_power WHERE user_id=%s", (id,))
        power = set([ x['power'] for x in res ])
        self.rs.set('user_power@%s' % str(id), power)
        return (None, power)

    def post_user_power(self, id, power):
        err, current_power = yield from self.get_user_power_info(id)
        if int(power) in current_power:
            yield from self.db.execute("DELETE FROM map_user_power WHERE user_id=%s and power=%s", (id, power,))
        else:
            yield from self.db.execute("INSERT INTO map_user_power (user_id, power) VALUES (%s, %s)", (id, power,))

    def get_user_group_power_info(self, uid, gid):
        res = self.rs.get('user_group_power@%s@%s' % (str(uid), str(gid)))
        if res: return (None, res)
        res = yield from self.db.execute("SELECT `power` from map_group_user_power where user_id=%s AND group_id=%s", (uid, gid,))
        power = set([x['power'] for x in res])
        self.rs.set('user_group_power@%s@%s' % (str(uid), str(gid)), power)
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
        err = self.check_required_args(required_args, data)
        if err: return (err, None)

        ### get hashed passwd
        col = ['passwd', 'id']
        sql = self.gen_select_sql('users', col)
        res = yield from self.db.execute(sql+
                'WHERE `account` = %s;',
                (data['account'],))
        ### check account 
        if len(res) == 0:
            return ('Euser', None)
        hpwd, id = res[0]["passwd"], res[0]["id"]
        ### check passwd
        if _hash(data['passwd']) != hpwd:
            return ('Epasswd', None)
        req.set_secure_cookie('id', str(id))
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
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        ### check data valadation
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
                (data['account'],))
        if len(res) == 0:
            return ('Ecreate', None)
        id = res[0]["id"]
        self.rs.delete('user_list_count')
        return (None, str(id))

