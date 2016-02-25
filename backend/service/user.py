from service.base import BaseService
from utils.form import form_validation
import hashlib
import config
import time
import random
import datetime

class UserService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        UserService.inst = self

    def hash_pwd(self, pwd):
        hpwd = hashlib.sha512(str(pwd).encode()).hexdigest() + config.PASSWORD_SALT
        hpwd = hashlib.md5(str(pwd).encode()).hexdigest()
        return hpwd

    def gen_token(self, account):
        token = "%s"%hashlib.md5(("%s@%s"%(account, str(time.time()))).encode()).hexdigest()
        token = 'NCTUOJ@%s@'%abs(hash(account)) + ''.join( _ if random.random() < 0.5 else _.upper() for _ in token)
        return token


    def get_user_list(self, data={}):
        required_args = [{
            'name': '+page',
            'type': int,
        }, {
            'name': '+count',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = (yield self.db.execute("SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s", (data['count'], (int(data['page'])-1)*int(data['count']),))).fetchall()
        for x in res:
            err, x["power"] = yield from self.get_user_power_info(x)
        return (None, res)

    def get_user_list_count(self, data={}):
        res = yield self.db.execute("SELECT COUNT(*) FROM users")
        res = res.fetchone()
        return (None, res['count'])

    def post_user_group_priority(self, data={}):
        required_args = ['id', 'group_list']
        pass

    def get_user_basic_info(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT u.*, s.name as school FROM users as u, schools as s where u.id=%s AND u.school_id = s.id", (data['id'],))
        if res.rowcount == 0:
            return ('ID Not Exist', None)
        res = res.fetchone()
        res.pop("passwd")
        err, res['power'] = yield from self.get_user_power_info(data)
        return (None, res)

    def get_user_basic_info_by_token(self, data={}):
        required_args = [{
            'name': '+token',
            'type': str
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = None
        if not res:
            res = yield self.db.execute("SELECT id FROM users WHERE token=%s", (data['token'],))
            if res.rowcount == 0:
                return ('Token Not Exist', None)
            res = res.fetchone()
        err, data = yield from self.get_user_basic_info(res)
        if err: return (err, None)
        return (None, data)

    def put_user_basic_info(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+passwd',
            'type': str,
        }, {
            'name': 'npasswd',
            'type': str,
        }, {
            'name': 'rpasswd',
            'type': str,
        }, {
            'name': 'name',
            'type': str,
        }, {
            'name': 'school_id',
            'type': int,
        }, {
            'name': 'email',
            'type': str,
        }, {
            'name': 'student_id',
            'type': str,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        id = data.pop('id')
        passwd = data.pop('passwd')
        npasswd = data.pop('npasswd')
        rpasswd = data.pop('rpasswd')
        res = yield self.db.execute('SELECT passwd FROM users WHERE id=%s;', (id,))
        if res.rowcount == 0: return ('User id not exist', None)
        hpasswd = res.fetchone()['passwd']
        if self.hash_pwd(passwd) != hpasswd: return ('Wrong Password', None)
        if npasswd is not None and npasswd != '':
            if npasswd != rpasswd:
                return ('Confirm new password', None)
            else: data['passwd'] = self.hash_pwd(npasswd)
        sql, param = self.gen_update_sql('users', data)
        res = yield self.db.execute(sql+' WHERE id=%s RETURNING token;', param+(id,))
        return (None, id)

    def get_user_advance_info_by_id(self, id):
        pass

    def get_user_advance_info_by_token(self, token):
        pass

    def get_user_group_info(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT g.* FROM groups as g, map_group_user as m where m.user_id=%s and g.id=m.group_id ORDER BY g.id", (data['id'],))
        res = res.fetchall()
        return (None, res)

    def get_user_power_info(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT power from map_user_power WHERE user_id=%s", (data['id'],))
        power = list({ x['power'] for x in res })
        return (None, power)

    def post_user_power(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+power',
            'type': int,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        err, current_power = yield from self.get_user_power_info(data)
        if int(data['power']) in current_power:
            yield self.db.execute("DELETE FROM map_user_power WHERE user_id=%s and power=%s", (data['id'], data['power'],))
        else:
            yield self.db.execute("INSERT INTO map_user_power (user_id, power) VALUES (%s, %s)", (data['id'], data['power'],))

    def get_user_contest(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('SELECT contest_id FROM map_contest_user WHERE user_id=%s;', (data['id'],))
        res = list({x['contest_id'] for x in res})
        return (None, res)

    def get_user_current_contest(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('SELECT c.* FROM map_contest_user as m, contests as c WHERE m.user_id=%s AND m.contest_id=c.id AND c.start<=%s AND %s<=c.end;', (data['id'], datetime.datetime.now(), datetime.datetime.now(),))
        if res.rowcount == 0:
            return (None, None)
        else:
            return (None, res.fetchone())

    def SignIn(self, data, req): #need to set cookie
        '''
        data(dict): account(str), passwd(str)
        return id(str)
        '''
        ### check required arguemts
        required_args = [{
            'name': '+account',
            'type': str,
        }, {
            'name': '+passwd',
            'type': str,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)

        ### get hashed passwd
        col = ['passwd', 'id', 'token']
        sql = self.gen_select_sql('users', col)
        res = yield self.db.execute(sql+' WHERE account = %s;', (data['account'],))
        ### check account 
        print('RESCNT', res.rowcount)
        if res.rowcount == 0:
            return ('User Not Exist', None)
        res = res.fetchone()
        hpwd, id, token = res["passwd"], res["id"], res['token']
        ### check passwd
        if self.hash_pwd(data['passwd']) != hpwd:
            return ('Wrong Password', None)
        print(token)
        req.set_secure_cookie('token', token)
        return (None, str(id))

    def SignOut(self, req):
        req.clear_cookie('token')

    def SignUp(self, data={}):
        '''
        data(dict): account(str), student_id(str), passwd(str), repasswd(str), email(str), school_id
        return id(str)
        '''
        ### check required arguemts
        required_args = [{
            'name': '+email',
            'type': str,
            'non_empty': True,
        }, {
            'name': '+account',
            'type': str,
            'non_empty': True,
        }, {
            'name': '+passwd',
            'type': str,
            'non_empty': True,
        }, {
            'name': '+repasswd',
            'type': str,
            'non_empty': True,
        },]
        err = form_validation(data, required_args)
        if err: return (err, None)
        ### check data valadation
        if data['passwd'] != data['repasswd']:
            return ('Confirm Two Password', None)


        ### check conflict
        res = yield self.db.execute('SELECT * FROM users WHERE account = %s or email = %s', (data['account'], data['email']))
        if res.rowcount != 0:
            res = res.fetchone()
            if res['email'] == data['email']:
                return ('Email Exist', None)
            elif res['account'] == data['account']:
                return ('Account Exist', None)

        ### gen hashed passwd
        hpasswd = self.hash_pwd(data['passwd'])
        ### gen sql query
        data['passwd'] = hpasswd
        data['token'] = self.gen_token(data['account'])
        data.pop('repasswd')
        sql, prama = self.gen_insert_sql('users', data)
        res = yield self.db.execute(sql, prama)
        res = yield self.db.execute('SELECT id FROM users '
                'WHERE account = %s', (data['account'],))
        if res.rowcount == 0:
            return ('Something Wrong!!!', None)
        id = res.fetchone()["id"]
        yield self.db.execute("INSERT INTO map_group_user (group_id, user_id) values (1, %s)", (id,))
        # self.rs.delete('user_list_count')
        return (None, str(id))

    def ResetToken(self, data):
        required_args = [{
            'name': '+account',
            'type': dict,
        }, {
            'name': '+passwd',
            'type': str,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        id = data['account']['id']
        token = data['account']['token']
        sql = self.gen_select_sql('users', ['account', 'passwd'])
        res = yield self.db.execute(sql + ' WHERE id = %s;', (id,))
        if res.rowcount == 0:
            return ('ID Not Exist', None)
        res = res.fetchone()
        hpasswd = res['passwd']
        account = res['account']
        if self.hash_pwd(data['passwd']) != hpasswd:
            return ('Passwd Error', None)
        # self.rs.delete("user_basic@%s" % id)
        # self.rs.delete("user_token@%s" % token)
        token = self.gen_token(account)
        sql, prama = self.gen_update_sql('users', {'token': token})
        res = yield self.db.execute(sql + ' WHERE id = %s;', prama + (id,))
        return (None, token)
    
    def delete_user(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('DELETE FROM users WHERE id=%s;', (data['id'], ))
        if res.rowcount == 0: return ('No such user', None)
        return (None, data['id'])
    def get_user_info_by_account_passwd(self, data={}):
        required_args = [{
            'name': '+account',
            'type': str,
        }, {
            'name': '+passwd',
            'type': str,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)

        ### get hashed passwd
        col = ['passwd', 'id', 'token']
        sql = self.gen_select_sql('users', col)
        res = yield self.db.execute(sql+' WHERE account = %s;', (data['account'],))
        ### check account 
        if res.rowcount == 0:
            return ('User Not Exist', None)
        res = res.fetchone()
        hpwd, id, token = res["passwd"], res["id"], res['token']
        ### check passwd
        if self.hash_pwd(data['passwd']) != hpwd:
            return ('Wrong Password', None)
        return (None, {
            'id': id,
            'token': token
        })
