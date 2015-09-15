from service.base import BaseService
import hashlib
import config
import time
import random
import datetime

class UserService(BaseService):

    def hash_pwd(self, pwd):
        hpwd = hashlib.sha512(str(pwd).encode()).hexdigest() + config.PASSWORD_KEY
        hpwd = hashlib.md5(str(pwd).encode()).hexdigest()
        return hpwd

    def gen_token(self, account):
        token = "%s"%hashlib.md5(("%s@%s"%(account, str(time.time()))).encode()).hexdigest()
        token = 'TOKEN@%s@'%account + ''.join( _ if random.random() < 0.5 else _.upper() for _ in token)
        return token

    def __init__(self, db, rs):
        super().__init__(db, rs)
        UserService.inst = self

    def get_user_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        res, res_cnt = yield from self.db.execute("SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s", (data['count'], (int(data['page'])-1)*int(data['count']),))
        for x in res:
            err, x["power"] = yield from self.get_user_power_info(x["id"])
        return (None, res)

    def get_user_list_count(self, data={}):
        res = self.rs.get('user_list_count')
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT COUNT(*) FROM users")
        self.rs.set('user_list_count', res[0]['count'])
        return (None, res[0]['count'])

    def get_user_basic_info(self, id):
        res = self.rs.get("user_basic@%s" % str(id))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT * FROM users where id=%s", (id,))
        if res_cnt == 0:
            return ('ID Not Exist', None)
        res = res[0]
        res.pop("passwd")
        err, res['power'] = yield from self.get_user_power_info(id)
        self.rs.set("user_basic@%s" % str(id), res)
        return (None, res)

    def get_user_basic_info_by_token(self, token):
        res = self.rs.get("user_token@%s" % token)
        if not res:
            res, res_cnt = yield from self.db.execute("SELECT id FROM users WHERE token=%s", (token,))
            if res_cnt == 0:
                return ('Token Not Exist', None)
            res = res[0]['id']
            self.rs.set("user_token@%s" % token, res)
        err, data = yield from self.get_user_basic_info(res)
        if err: return (err, None)
        return (None, data)

    def get_user_advance_info_by_id(self, id):
        pass

    def get_user_advance_info_by_token(self, token):
        pass

    def get_user_group_info(self, id):
        res = self.rs.get('user_group@%s' % str(id))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT g.* FROM groups as g, map_group_user as m where m.user_id=%s and g.id=m.group_id ORDER BY g.id", (id,))
        self.rs.set('user_group@%s' % str(id), res)
        return (None, res)

    def get_user_power_info(self, id):
        res = self.rs.get('user_power@%s' % str(id))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT power from map_user_power WHERE user_id=%s", (id,))
        power = list({ x['power'] for x in res })
        self.rs.set('user_power@%s' % str(id), power)
        return (None, power)

    def post_user_power(self, id, power):
        err, current_power = yield from self.get_user_power_info(id)
        self.rs.delete('user_power@%s'%(str(id)))
        if int(power) in current_power:
            yield from self.db.execute("DELETE FROM map_user_power WHERE user_id=%s and power=%s", (id, power,))
        else:
            yield from self.db.execute("INSERT INTO map_user_power (user_id, power) VALUES (%s, %s)", (id, power,))

    def get_user_group_power_info(self, uid, gid):
        res = self.rs.get('user_group_power@%s@%s' % (str(uid), str(gid)))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT power from map_group_user_power where user_id=%s AND group_id=%s", (uid, gid,))
        power = list({ x['power'] for x in res })
        self.rs.set('user_group_power@%s@%s' % (str(uid), str(gid)), power)
        return (None, power)

    def post_user_group_power(self, uid, gid, power):
        current_power = yield from self.get_user_group_power_info(uid, gid)
        if int(power) in current_power:
            yield from self.db.execute('DELETE FROM map_group_user_power WHERE user_id=%s AND group_id=%s AND power=%s;', (uid, gid, power,))
        else:
            yield from self.db.execute('INSERT INTO map_group_user_power (user_id, group_id, power) VALUES(%s, %s, %s);', (uid, gid, power))

    def modify(self, data={}):
        pass

    def get_user_contest(self, id):
        #res = self.rs.get('user@%scontest'%(str(id)))
        #if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT id FROM map_contest_user WHERE user_id=%s;', (id,))
        res = set(x['id'] for x in res)
        return (None, res)

    def get_user_current_contest(self, id):
        res, res_cnt = yield from self.db.execute('SELECT c.* FROM map_contest_user as m, contests as c WHERE m.user_id=%s AND m.contest_id=c.id AND c.start<=%s AND %s<=c.end;', (id, datetime.datetime.now(), datetime.datetime.now(),))
        if res_cnt == 0:
            return (None, None)
        else:
            return (None, res[0])

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
        res, res_cnt = yield from self.db.execute(sql+' WHERE account = %s;', (data['account'],))
        ### check account 
        print('RESCNT', res_cnt)
        if res_cnt == 0:
            return ('User Not Exist', None)
        print('=========================')
        print(res)
        hpwd, id = res[0]["passwd"], res[0]["id"]
        ### check passwd
        if self.hash_pwd(data['passwd']) != hpwd:
            return ('Wrong Password', None)
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
            return ('Confirm Two Password', None)

        ### check conflict
        res, res_cnt = yield from self.db.execute('SELECT id FROM users ' 
                'WHERE account = %s OR student_id = %s', 
                (data['account'], data['student_id'],))
        if res_cnt != 0:
            return ('User Exist', None)

        ### gen hashed passwd
        hpasswd = self.hash_pwd(data['passwd'])
        ### gen sql query
        data['passwd'] = hpasswd
        data['token'] = self.gen_token(data['account'])
        data.pop('repasswd')
        sql, prama = self.gen_insert_sql('users', data)
        res, res_cnt = yield from self.db.execute(sql, prama)
        res, res_cnt = yield from self.db.execute('SELECT id FROM users '
                'WHERE account = %s', (data['account'],))
        if res_cnt == 0:
            return ('Something Wrong', None)
        id = res[0]["id"]
        self.rs.delete('user_list_count')
        return (None, str(id))

    def ResetToken(self, data):
        required_args = ['account', 'passwd']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        id = data['account']['id']
        token = data['account']['token']
        sql = self.gen_select_sql('users', ['account', 'passwd'])
        res, res_cnt = yield from self.db.execute(sql + ' WHERE id = %s;', (id,))
        if res_cnt == 0:
            return ('ID Not Exist', None)
        hpasswd = res[0]['passwd']
        account = res[0]['account']
        if self.hash_pwd(data['passwd']) != hpasswd:
            return ('Passwd Error', None)
        self.rs.delete("user_basic@%s" % id)
        self.rs.delete("user_token@%s" % token)
        token = self.gen_token(account)
        sql, prama = self.gen_update_sql('users', {'token': token})
        res, res_cnt = yield from self.db.execute(sql + ' WHERE id = %s;', prama + (id,))
        return (None, token)

