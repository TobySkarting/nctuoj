from req import Service
from service.base import BaseService
from utils.utils import HashPassword
from utils.utils import GenToken


class User(BaseService):
    def get_user(self, data):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM users WHERE id=%s", (data['id'],))
        res = res.fetchone()
        if res == None:
            return ((404, "User Not Exist"), None)
        res.pop('password')
        res.pop('token')
        return (None, res)

    def post_user(self, data):
        required_args = [{
            'name': '+email',
            'type': str,
        }, {
            'name': '+account',
            'type': str,
        }, {
            'name': '+password',
            'type': str,
        }, {
            'name': '+repassword',
            'type': str,
        }, {
            'name': '+name',
            'type': str,
        }]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        if data['password'] != data['repassword']:
            return ((400, "password is not equal to repassword"), None)
        ### check email

        ### check conflict
        res = yield self.db.execute('SELECT * FROM users WHERE account=%s or email=%s', (data['account'], data['email'],))
        if res.rowcount != 0:
            res = res.fetchone()
            if res['email'] == data['email']:
                return ((400, 'Email Exist'), None)
            elif res['account'] == data['account']:
                return ((400, 'Account Exist'), None)
        
        data.pop('repassword')
        data['token'] = GenToken(data)
        data['password'] = HashPassword(data['password'])
        sql, param = self.gen_insert_sql('users', data)
        res = yield self.db.execute(sql, param)
        res = res.fetchone()
        return (None, res)

    def delete_user(self, data):
        required_args = [{
            'name': '+id',
            'type': int,
        },]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        yield self.db.execute("DELETE FROM users WHERE id=%s", (data['id'],))
        return (None, None)

