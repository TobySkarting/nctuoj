from req import Service
from service.base import BaseService
from utils.utils import HashPassword


class Session(BaseService):
    def post_session_by_password(self, req, data):
        required_args = [{
            'name': '+account',
            'type': str,
        }, {
            'name': '+password',
            'type': str,
        }]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM users WHERE account=%s", (data['account'],))
        res = res.fetchone()
        if res == None:
            return ((404, "User Not Exist"), None)
        if res['password'] != HashPassword(data['password']):
            return ((403, "Wrong Password"), None)
        res.pop('password')
        req.set_secure_cookie('token', res['token'])
        return (None, res)

    def post_session_by_toekn(self, req, data):
        required_args = [{
            'name': '+token',
            'type': str,
        },]
        err = self.form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT * FROM users WHERE token=%s", (data['token'],))
        res = res.fetchone()
        if res == None:
            return ((404, "User Not Exist"), None)
        res.pop('password')
        req.set_secure_cookie('token', res['token'])
        return (None, res)

    def delete_session(self, req):
        req.clear_cookie('token')
        return (None, None)
